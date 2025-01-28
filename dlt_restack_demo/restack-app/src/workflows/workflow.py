from datetime import timedelta

from pydantic import BaseModel, Field
from restack_ai.workflow import import_functions, log, workflow

with import_functions():
    from src.functions.function import poke_pipeline


class GreetingWorkflowInput(BaseModel):
    name: str = Field(default="Bob")


@workflow.defn()
class GreetingWorkflow:
    @workflow.run
    async def run(self, input: GreetingWorkflowInput):
        log.info("GreetingWorkflow started")
        result = await workflow.step(
            poke_pipeline, start_to_close_timeout=timedelta(seconds=300)
        )
        log.info("GreetingWorkflow completed", result=result)
        return result
