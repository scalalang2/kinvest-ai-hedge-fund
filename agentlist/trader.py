from agent_framework import Executor, WorkflowContext, handler
from agent_framework.openai import OpenAIChatClient

from agentlist.messages import ResearchRequest, ResearchResultsResponse, RiskAssessmentRequest, StartTradingRequest

class Trader(Executor):
    """
    Trader 에이전트는 워크플로우의 시작점이자 나의 관심 개별 종목들을 리서치 팀에게 조사를 요청한 다음 
    리서치 팀의 결과를 종합해서 개별 종목에 대한 매수/매도 의견을 제시합니다.

    이를 리스크 매니저 팀에게 전달하여 리스크 평가를 받습니다.
    마지막으로 매니저가 현재 내가 가지고 있는 포트폴리오를 고려하여 최종 매수/매도 결정을 내리도록 합니다.
    """
    def __init__(self, model: OpenAIChatClient):
        super().__init__(id="Trader")
        self._model = model

    @handler
    async def handle_start_trding(self, request: StartTradingRequest, ctx: WorkflowContext[ResearchRequest]) -> None:
        await ctx.send_message(ResearchRequest())

    @handler
    async def handle_research_results(self, request: ResearchResultsResponse, ctx: WorkflowContext[RiskAssessmentRequest]) -> None:
        await ctx.send_message(RiskAssessmentRequest())