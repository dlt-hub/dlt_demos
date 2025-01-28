from datetime import timedelta

from pydantic import BaseModel, Field
from restack_ai.workflow import import_functions, log, workflow, RetryPolicy

with import_functions():
    from src.functions.function import anime_pipeline


class AnimePipelineInput(BaseModel):
    destination: str = Field(default="weaviate")


@workflow.defn()
class AnimePipeline:
    @workflow.run
    async def run(self, input: AnimePipelineInput):
        log.info("PokePipeline started")
        result = await workflow.step(
            anime_pipeline,
            input=input,
            start_to_close_timeout=timedelta(seconds=300),
            retry_policy=RetryPolicy(maximum_attempts=1)
        )
        log.info("PokePipeline completed", result=result)
        return result
