import traceback
from typing import Optional, Any

import dlt
from openai import OpenAI
from pydantic import BaseModel
from restack_ai.function import function, log


class RAGInput(BaseModel):
    pipeline_name: str
    question: str


openai_client = OpenAI(api_key=dlt.secrets["openai.api_key"])


@function.defn()
async def rag_pipeline(input: RAGInput) -> str:
    try:
        pipeline = dlt.pipeline(
            pipeline_name=input.pipeline_name,
            destination="weaviate",
            progress="log",
            dev_mode=False,
        )
        with pipeline.destination_client() as client:
            return rag_query(client.db_client, str(input))

    except Exception as e:
        log.error("Something went wrong!", error=e)
        log.error(traceback.format_exc())
        raise e


def rag_query(weaviate_client: Any, prompt: str) -> Optional[str]:
    response = (
        weaviate_client.query.get("Anime", ["title", "synopsis"])
        .with_near_text({"concepts": [prompt]})
        .with_limit(3)
        .do()
    )

    if "data" in response and "Get" in response["data"]:
        docs = response["data"]["Get"]["Anime"]
        print("Retrieved documents:")
        for doc in docs:
            print(f"- {doc['title']}: {doc['synopsis']}\n")
    else:
        print("No results found.")
        return None

    context = " ".join([doc["synopsis"] for doc in docs])

    completion = openai_client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=f"{context}\n\nQuestion: {prompt}\nAnswer:",
        max_tokens=150,
    )

    log.info("Generated Answer:")
    answer = completion.choices[0].text.strip()
    log.info(answer)
    return answer
