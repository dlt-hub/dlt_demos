from datetime import timedelta

from pydantic import BaseModel, Field
from restack_ai.workflow import RetryPolicy, import_functions, log, workflow

with import_functions():
    from src.functions.dlt_to_weaviate import anime_pipeline
    from src.functions.vector_search import rag_pipeline


class AnimePipelineInput(BaseModel):
    pipeline_name: str = Field(default="anime_pipeline")
    destination: str = Field(default="weaviate")
    add_limit: int = Field(default=2)
    dev_mode: bool = Field(default=False)


class RAGPipelineInput(BaseModel):
    pipeline_name: str = Field(default="anime_pipeline")
    question: str = Field(
        default="What is the story about Ye Bufan and his medical skills?"
    )


@workflow.defn()
class AnimePipeline:
    @workflow.run
    async def run(self, input: AnimePipelineInput):
        log.info("PokePipeline started")
        result = await workflow.step(
            anime_pipeline,
            input=input,
            start_to_close_timeout=timedelta(seconds=300),
            retry_policy=RetryPolicy(maximum_attempts=1),
        )
        log.info("PokePipeline completed", result=result)
        return result


@workflow.defn()
class RAGPipeline:
    @workflow.run
    async def run(self, input: RAGPipelineInput):
        log.info("RAGPipeline started")
        result = await workflow.step(
            rag_pipeline,
            input=input,
            start_to_close_timeout=timedelta(seconds=300),
            retry_policy=RetryPolicy(maximum_attempts=1),
        )
        log.info("RAGPipeline completed", result=result)
        return result
