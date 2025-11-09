import asyncio
from typing import Annotated, List

from agent_framework import (
    Executor,
    WorkflowContext,
    handler,
    ChatMessage,
    WorkflowEvent,
)

from agent_framework.openai import OpenAIChatClient

from agentlist.messages import ResearchRequest, ResearchResultsResponse, DebateResult
import kis


BULLISH_PROMPT = """
You are a financial analyst with a bullish outlook. Your analysis must be strictly based on quantitative data, technical indicators, and fundamental metrics from the provided context.
Analyze the provided stock data and present a concise, data-driven argument for why the stock is a 'BUY'.
When presenting your argument, you must also provide a confidence score (0.0 to 1.0) for your reasoning.
Counter the points made by the Bearish Analyst with data and charts.
Your response MUST be a JSON object with two keys: "reason" (your analysis as a string) and "confidence" (your score as a float).
"""

BEARISH_PROMPT = """
You are a financial analyst with a bearish outlook. Your analysis must be strictly based on quantitative data, technical indicators, and fundamental metrics from the provided context.
Analyze the provided stock data and present a concise, data-driven argument for why the stock is a 'SELL'.
Focus on risks, high valuation metrics (P/E), debt-to-equity ratio, and negative trends in technical indicators.
When presenting your argument, you must also provide a confidence score (0.0 to 1.0) for your reasoning.
Counter the points made by the Bullish Analyst with data and charts.
Your response MUST be a JSON object with two keys: "reason" (your analysis as a string) and "confidence" (your score as a float).
"""

SUMMARIZER_PROMPT = """
You are a senior investment strategist. You have been provided with a debate between a Bullish and a Bearish analyst.
Your task is to synthesize the entire debate. Objectively summarize the key arguments from both sides, citing specific data points they used.
Conclude with a final, balanced investment insight that weighs the bullish and bearish cases. Do not take a side. The summary should be neutral and informative.
"""

class BearishDebateEvent(WorkflowEvent):
    def __init__(self, message: str, confidence: float):
        super().__init__(f"Bearish Debate: {message}, Confidence: {confidence}")

class BullishDebateEvent(WorkflowEvent):
    def __init__(self, message: str, confidence: float):
        super().__init__(f"Bullish Debate: {message}, Confidence: {confidence}")

class Researcher(Executor):
    """
    Researcher는 개별 종목 코드를 전달받은 다음, 해당 종목에 대한 debate 방식의 리서치를 수행합니다.
    Bullish -> Bearish
    Bearish -> Bullish - N rounds
    Summarize the result
    """
    def __init__(self, model: OpenAIChatClient):
        super().__init__(id="researcher")
        self._model = model

    @handler
    async def run_debate(self, request: ResearchRequest, ctx: WorkflowContext[ResearchResultsResponse]) -> None:
        bullish_agent, bearish_agent, summarizer = self._setup_agents()

        num_round = 2
        current_speaker = "Bullish"
        initial_prompt = f"""
            Start the debate for stock code: {request.stock_code}, stock name: {request.stock_name}. 
            Present your initial bullish case based on available data."""
        conversation_history: List[ChatMessage] = [ChatMessage(role="user", text=initial_prompt)]
        debate_history = []

        for round in range(num_round*2):
            if current_speaker == "Bullish":
                agent = bullish_agent
                response = await agent.run(conversation_history)

                debate_result = DebateResult.model_validate_json(response.text)
                debate_result.speaker = current_speaker
                debate_history.append(debate_result)
                conversation_history.append(ChatMessage(
                    role="assistant",
                    text=f"speaker: {current_speaker}, reason: {debate_result.reason}, confidence: {debate_result.confidence}"
                ))
                conversation_history.append(ChatMessage(
                    role="user",
                    text="Please respond to the previous argument with your bearish perspective."
                ))

                current_speaker = "Bearish"
                await ctx.add_event(BullishDebateEvent(debate_result.reason, debate_result.confidence))
            else:
                agent = bearish_agent
                response = await agent.run(conversation_history)

                debate_result = DebateResult.model_validate_json(response.text)
                debate_result.speaker = current_speaker
                debate_history.append(debate_result)
                conversation_history.append(ChatMessage(
                    role="assistant",
                    text=f"speaker: {current_speaker}, reason: {debate_result.reason}, confidence: {debate_result.confidence}"
                ))
                conversation_history.append(ChatMessage(
                    role="user",
                    text="Please respond to the previous argument with your bullish perspective."
                ))

                current_speaker = "Bullish"
                await ctx.add_event(BearishDebateEvent(debate_result.reason, debate_result.confidence))

        conversation_history.append(ChatMessage(
            role="user",
            text=SUMMARIZER_PROMPT,
        ))
        summary = await summarizer.run(conversation_history)

        response = ResearchResultsResponse(
            stock_code=request.stock_code,
            debate_history=debate_history,
            summarized=summary.text,
        )
        await ctx.send_message(response)

    def _setup_agents(self):
        bullish_agent = self._model.create_agent(
            name="Bullish Analyst",
            instructions=[BULLISH_PROMPT],
            tools=[self.get_stock_chart],
            response_format=DebateResult,
        )

        bearish_agent = self._model.create_agent(
            name="Bearish Analyst",
            instructions=[BEARISH_PROMPT],
            tools=[self.get_stock_chart],
            response_format=DebateResult,
        )

        summarizer = self._model.create_agent(
            name="Research Summarizer",
        )

        return bullish_agent, bearish_agent, summarizer

    def get_stock_chart(
        stock_code: Annotated[str, "종목 코드"],
        range: Annotated[str, "조회 기간 범위 ('1d', '5d', '1m', '3m', '6m', '1y', '2y', '5y')"],
        period: Annotated[str, "조회 주기 (숫자]): 분단위, 'day', 'week', 'month', 'year' 등)"]):
        client = kis.create_kis()
        result = client.stock(stock_code).chart(range, period=period)
        return result