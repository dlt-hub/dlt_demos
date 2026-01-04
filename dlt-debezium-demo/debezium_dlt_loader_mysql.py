"""
MySQL CDC Loader: Debezium + dlt Integration

Captures changes from MySQL using Embedded Debezium Engine and loads them into dlt.
"""
import json
import logging
import signal
import sys
import queue
import threading
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Any

import dlt
from pydbzengine import BasePythonChangeHandler, ChangeEvent, DebeziumJsonEngine, Properties

from config_helper_universal import generate_debezium_properties_file


def setup_logging():
    """Configure logging for the CDC pipeline."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


logger = logging.getLogger(__name__)

# Global thread-safe queue for decoupling Java callbacks from Python execution
event_queue = queue.Queue()


class DltChangeHandler(BasePythonChangeHandler):
    """
    Handles Debezium change events.
    OPTIMIZATION: Batches all table loads into a single atomic transaction.
    Uses dlt transformers for zero-copy event enrichment.
    """
    LOGGER_NAME = "debeziumdlt.DltChangeHandler"
    
    def __init__(self):
        self.log = logging.getLogger(self.LOGGER_NAME)
    
    def handleJsonBatch(self, records: List[ChangeEvent]) -> None:
        """
        Process batch of CDC events.
        Groups events by table and runs ONE pipeline job for efficiency.
        """
        if not records:
            return
        
        # Extract values immediately (ChangeEvent may be tied to JNI resources)
        safe_records = []
        for r in records:
            try:
                # Extract key/value strings
                safe_records.append({
                    "key": r.key(),
                    "value": r.value(),
                    "destination": r.destination()
                })
            except Exception as e:
                self.log.error(f"Error extracting record data: {e}")

        if safe_records:
            self.log.debug(f"Queuing {len(safe_records)} records")
            event_queue.put(safe_records)


def parse_event(record_dict: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Parses Debezium JSON.
    The preceding 'delete' event (op='d') already contained the data we needed.
    """
    # 1. Ignore Tombstones (Value is None)
    if record_dict["value"] is None:
        return None
    
    try:
        # 2. Parse Standard Event
        value_data = json.loads(record_dict["value"])
        payload = value_data.get("payload", {})
        
        op = payload.get("op")
        # 'd' uses 'before' (state before delete), others use 'after'
        data = payload.get("before" if op == "d" else "after")
        
        if not data:
            return None
        
        source = payload.get("source", {})
        
        return {
            "op": op,
            "table": source.get("table"),
            "payload": data,
        }
    except Exception as e:
        logger.error(f"Error parsing event: {e}")
        return None


def create_resource(table_name: str, events: List[Dict[str, Any]], primary_keys: Dict[str, str]) -> Any:
    """
    Create dlt resource with Merge/Append logic.
    Uses dlt transformer pattern for zero-copy event enrichment.
    """
    primary_key = primary_keys.get(table_name)
    
    mode = "merge" if primary_key else "append"
    
    def enrich_event(event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform event for dlt loading.
        Zero-copy: Mutates payload in-place since we own the dict.
        """
        row = event["payload"]
        row["__table"] = table_name
        
        if mode == "merge":
            row["__deleted"] = (event["op"] == "d")
        else:
            row["__op"] = "delete" if event["op"] == "d" else event["op"]
        
        return row
    
    # Create resource from events list
    resource = dlt.resource(events, name=table_name, write_disposition=mode)
    resource.add_map(enrich_event)
    
    if mode == "merge":
        resource.apply_hints(primary_key=primary_key)
    
    return resource


def process_queue(pipeline: dlt.Pipeline, primary_keys: Dict[str, str], stop_event: threading.Event):
    """Main loop that consumes events from the queue and runs the pipeline."""
    logger.info("Queue consumer started. Waiting for events...")
    
    while not stop_event.is_set():
        try:
            # Wait for batch with timeout to allow checking stop_event
            records = event_queue.get(timeout=1.0)
        except queue.Empty:
            continue
            
        try:
            # 1. Parse and Group
            events_by_table = defaultdict(list)
            for record in records:
                event_data = parse_event(record)
                if event_data and event_data.get("table"):
                    events_by_table[event_data["table"]].append(event_data)
            
            if not events_by_table:
                continue
            
            logger.info(f"Processing batch: {len(records)} events across {len(events_by_table)} tables")

            # 2. Create Resources
            resources = []
            for table_name, events in events_by_table.items():
                resources.append(create_resource(table_name, events, primary_keys))
            
            # 3. Execute load (runs in main thread)
            load_info = pipeline.run(resources)
            logger.info(f"✅ Batch load complete: {load_info}")
            
            # Sync to ensure data is written and locks are released
            try:
                pipeline.sync_destination()
            except Exception as sync_err:
                logger.debug(f"Sync destination note: {sync_err}")
                
        except Exception as e:
            logger.error(f"❌ Batch load failed: {e}", exc_info=True)
            try:
                pipeline.sync_destination()
            except:
                pass
        finally:
            event_queue.task_done()


def load_properties(filepath: Path) -> Properties:
    """Load Java .properties file into a dictionary-like object."""
    props = Properties()
    if not filepath.exists():
        return props
    
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                props.setProperty(key.strip(), value.strip())
    return props


def main() -> None:
    setup_logging()
    logger.info("Starting MySQL CDC Pipeline: Debezium + dlt")
    
    # Primary keys for merge operations (configurable via .dlt/config.toml)
    primary_keys = dlt.config.get("cdc_settings.primary_keys", {})
    
    # Setup Debezium Config
    props_file = generate_debezium_properties_file(
        connector_class="io.debezium.connector.mysql.MySqlConnector",
        db_config_section="sources.debezium.mysql",
    )
    
    # Init pipeline (dlt auto-reads credentials from .dlt/secrets.toml)
    pipeline = dlt.pipeline(
        pipeline_name="mysql_cdc",
        destination="duckdb",
        dataset_name="mysql_cdc_data",
    )
    logger.info(f"✅ Pipeline Active: mysql_cdc → mysql_cdc_data")
    
    if primary_keys:
        logger.info(f"Keys Configured: {list(primary_keys.keys())}")
    else:
        logger.info("Using APPEND mode (no primary keys configured)")

    # Start Debezium in background thread (it blocks, so dlt runs in main thread)
    stop_event = threading.Event()
    
    # Init Debezium
    props = load_properties(props_file)
    handler = DltChangeHandler()
    engine = DebeziumJsonEngine(props, handler)
    
    def run_engine():
        try:
            engine.run()
        except Exception as e:
            logger.error(f"Engine crashed: {e}")
    
    engine_thread = threading.Thread(target=run_engine, name="DebeziumEngineThread")
    engine_thread.daemon = True
    engine_thread.start()
    
    # Register signal handlers
    def signal_handler(sig, frame):
        logger.info(f"\nSignal {sig} received. Stopping...")
        stop_event.set()
        try:
            engine.interrupt() 
        except:
            pass
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Run queue processor in main thread (dlt runs here for thread safety)
    try:
        process_queue(pipeline, primary_keys, stop_event)
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    finally:
        logger.info("Pipeline shutdown complete")


if __name__ == "__main__":
    main()
