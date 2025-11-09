from agent_framework import Executor, WorkflowContext, handler
from agent_framework.openai import OpenAIChatClient

from agentlist.messages import RiskAssessmentRequest, RiskAssessmentResult

class RiskManagerConservative(Executor):
    """
    보수적인 투자를 권유하는 리스크 매니저
    """
    def __init__(self, model: OpenAIChatClient):
        super().__init__(id="risk_amanger_conservative")
        self._model = model

    @handler
    async def handle_risk_assessment(self, request: RiskAssessmentRequest, ctx: WorkflowContext[RiskAssessmentResult]) -> None:
        await ctx.send_message(RiskAssessmentResult())