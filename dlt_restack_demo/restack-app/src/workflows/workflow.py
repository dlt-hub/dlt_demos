from datetime import timedelta

from restack_ai.workflow import import_functions, log, workflow

with import_functions():
    from src.functions.function import poke_pipeline


@workflow.defn()
class PokePipeline:
    @workflow.run
    async def run(self):
        log.info("PokePipeline started")
        result = await workflow.step(
            poke_pipeline, start_to_close_timeout=timedelta(seconds=300)
        )
        log.info("PokePipeline completed", result=result)
        return result
