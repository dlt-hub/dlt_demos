import json
import html as html_module
import sys

import dlt
import anthropic
from dlt.hub import run
from dlt.sources.helpers import requests

HN_BASE = "https://hacker-news.firebaseio.com/v0"


def get_current_hiring_thread() -> int:
    """Find the most recent 'Ask HN: Who is Hiring?' thread via Algolia search."""
    resp = requests.get(
        "https://hn.algolia.com/api/v1/search",
        params={
            "query": "Ask HN: Who is hiring?",
            "tags": "ask_hn,author_whoishiring",
            "hitsPerPage": 1,
        }
    )
    resp.raise_for_status()
    hits = resp.json().get("hits", [])
    if not hits:
        raise ValueError("Could not find a 'Who is Hiring' thread via Algolia")
    thread_id = int(hits[0]["objectID"])
    title = hits[0].get("title", "unknown")
    print(f"Found thread: {title!r} (ID: {thread_id})")
    return thread_id


TOOL_EXTRACT_PROMPT = """\
You are a data stack analyst. Read this HackerNews job posting and extract tool/technology information.

Comment:
{text}

Return ONLY a JSON object with these exact fields:
{{
  "named_tools": ["array of named software products, tools, platforms, databases, frameworks — e.g. Snowflake, dbt, Airflow, Kafka, Pinecone, LangChain. Include ALL named products you can identify."],
  "has_custom_tooling": true/false,
  "custom_tooling_notes": "brief description of any custom/homegrown/unnamed internal tools mentioned, or null"
}}

Rules:
- named_tools: only specific product/tool names, not generic skills like 'SQL' or 'Python'
- Include cloud providers (AWS, GCP, Azure) and their specific services (e.g. S3, BigQuery, Redshift)
- Include AI/LLM tools (LangChain, Pinecone, Weaviate, pgvector, OpenAI, Anthropic, etc.)
- has_custom_tooling: true if the post mentions custom-built, homegrown, or internal tooling
- Return ONLY the JSON object, no markdown fences, no explanation."""

EXTRACT_PROMPT = """\
You are a job posting parser. Extract structured information from this HackerNews "Who is Hiring" comment.

Comment:
{text}

Return ONLY a JSON object with these exact fields (use null if not present):
{{
  "company_name": "string or null",
  "role": "string or null",
  "location": "string or null",
  "is_remote": true/false/null,
  "salary": "string or null (raw salary text, e.g. '$120k-$150k')",
  "skills": ["array", "of", "strings"],
  "summary": "1-2 sentence plain-text summary or null"
}}

Return ONLY the JSON object, no markdown fences, no explanation."""


@dlt.resource(name="raw_comments", write_disposition="merge", primary_key="id")
def raw_comments(
    thread_id: int,
    last_id: dlt.sources.incremental[int] = dlt.sources.incremental("id", initial_value=0),
):
    thread_resp = requests.get(f"{HN_BASE}/item/{thread_id}.json")
    thread_resp.raise_for_status()
    thread = thread_resp.json()

    comment_ids = thread.get("kids", [])
    for comment_id in comment_ids:
        resp = requests.get(f"{HN_BASE}/item/{comment_id}.json")
        if resp.status_code != 200:
            continue
        item = resp.json()
        if not item or item.get("deleted") or item.get("dead"):
            continue
        item["text"] = html_module.unescape(item.get("text", "") or "")
        item["thread_id"] = thread_id
        yield item  # dlt filters out ids already seen


@dlt.source(name="hackernews_hiring")
def hackernews_hiring_source(
    thread_id: int,
    anthropic_api_key: str = dlt.secrets.value,
):
    @dlt.transformer(
        data_from=raw_comments(thread_id),
        name="tool_extractions",
        write_disposition="merge",
        primary_key="comment_id",
    )
    def extract_tool_mentions(comment):
        text = comment.get("text", "").strip()
        base = {
            "comment_id": comment["id"],
            "by": comment.get("by"),
            "time": comment.get("time"),
            "thread_id": comment.get("thread_id"),
        }
        if len(text) < 20:
            yield {**base, "named_tools": [], "has_custom_tooling": False, "custom_tooling_notes": None}
            return
        client = anthropic.Anthropic(api_key=anthropic_api_key)
        try:
            response = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=256,
                messages=[{"role": "user", "content": TOOL_EXTRACT_PROMPT.format(text=text[:4000])}],
            )
            raw = response.content[0].text.strip()
            if raw.startswith("```"):
                raw = raw.split("```")[1].lstrip("json").strip()
            extracted = json.loads(raw)
            if not isinstance(extracted.get("named_tools"), list):
                extracted["named_tools"] = []
            yield {**base, **extracted}
        except Exception as exc:
            yield {**base, "named_tools": [], "has_custom_tooling": False,
                   "custom_tooling_notes": None, "parse_error": str(exc)}

    @dlt.transformer(
        data_from=raw_comments(thread_id),
        name="job_posts",
        write_disposition="merge",
        primary_key="comment_id",
    )
    def extract_job_info(comment):
        text = comment.get("text", "").strip()
        base = {
            "comment_id": comment["id"],
            "by": comment.get("by"),
            "time": comment.get("time"),
            "thread_id": comment.get("thread_id"),
            "raw_text": text,
        }
        if len(text) < 20:
            yield {**base, "company_name": None, "role": None, "location": None,
                   "is_remote": None, "salary": None, "skills": [], "summary": None,
                   "parse_error": "text too short"}
            return
        client = anthropic.Anthropic(api_key=anthropic_api_key)
        try:
            response = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=1024,
                messages=[{"role": "user", "content": EXTRACT_PROMPT.format(text=text[:4000])}],
            )
            raw = response.content[0].text.strip()
            if raw.startswith("```"):
                raw = raw.split("```")[1].lstrip("json").strip()
            extracted = json.loads(raw)
            if isinstance(extracted, list):
                extracted = extracted[0] if extracted else {}
            if not isinstance(extracted, dict):
                raise ValueError(f"Expected JSON object, got {type(extracted).__name__}")
            if not isinstance(extracted.get("skills"), list):
                extracted["skills"] = []
            yield {**base, **extracted, "parse_error": None}
        except Exception as exc:
            yield {**base, "company_name": None, "role": None, "location": None,
                   "is_remote": None, "salary": None, "skills": [], "summary": None,
                   "parse_error": str(exc)}

    return extract_tool_mentions, extract_job_info


@run.pipeline("hackernews_hiring", trigger="0 9 1,15 * *")
def run_pipeline():
    thread_id = get_current_hiring_thread()
    pipeline = dlt.pipeline(
        pipeline_name="hackernews_hiring",
        destination="warehouse",
        dataset_name="hn_hiring",
    )
    pipeline.run(hackernews_hiring_source(thread_id))


if __name__ == "__main__":
    # Allow overriding thread ID for backfilling: --thread-id 47601859
    if "--thread-id" in sys.argv:
        idx = sys.argv.index("--thread-id")
        thread_id = int(sys.argv[idx + 1])
        print(f"Using specified thread ID: {thread_id}")
    else:
        thread_id = get_current_hiring_thread()

    pipeline = dlt.pipeline(
        pipeline_name="hackernews_hiring",
        destination="warehouse",
        dataset_name="hn_hiring",
    )

    if "--raw" in sys.argv:
        load_info = pipeline.run(raw_comments(thread_id))
        print(load_info)
        sys.exit(0)

    load_info = pipeline.run(hackernews_hiring_source(thread_id))
    print(load_info)
