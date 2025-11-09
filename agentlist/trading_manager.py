from typing import List
from agent_framework import Executor, WorkflowContext, handler
from agent_framework.openai import OpenAIChatClient

from agentlist.messages import RiskAssessmentResult

class TradingManager(Executor):
    """
    TradingManager는 RiskManager의 종합 의견을 고려해서 포트폴리오 변경을 결정합니다.
    """
    def __init__(self, model: OpenAIChatClient):
        super().__init__(id="trading_manager")
        self._model = model

    @handler
    async def handle_start_trding(self, request: List[RiskAssessmentResult], ctx: WorkflowContext) -> None:
        pass