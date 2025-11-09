from agent_framework import Executor, WorkflowContext, handler
from agent_framework.openai import OpenAIChatClient

from agentlist.messages import ResearchRequest, ResearchResultsResponse


class Researcher(Executor):
    """
    Researcher는 개별 종목 코드를 전달받은 다음, 해당 종목에 대한 debate 방식의 리서치를 수행합니다.
    """
    def __init__(self, model: OpenAIChatClient):
        super().__init__(id="researcher")
        self._model = model

    @handler
    async def handle_start_trding(self, request: ResearchRequest, ctx: WorkflowContext[ResearchResultsResponse]) -> None:
        await ctx.send_message(ResearchResultsResponse())