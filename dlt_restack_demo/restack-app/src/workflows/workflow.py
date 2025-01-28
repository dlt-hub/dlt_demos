from datetime import timedelta

from pydantic import BaseModel, Field
from restack_ai.workflow import import_functions, log, workflow

with import_functions():
    from src.functions.function import poke_pipeline


class PokePipelineInput(BaseModel):
    name: str = Field(default="Bob")


@workflow.defn()
class PokePipeline:
    @workflow.run
    async def run(self, input: PokePipelineInput):
        log.info("PokePipeline started")
        result = await workflow.step(
            poke_pipeline, start_to_close_timeout=timedelta(seconds=300)
        )
        log.info("PokePipeline completed", result=result)
        return result
