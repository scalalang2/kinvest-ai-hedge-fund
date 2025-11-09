from typing import Annotated, List
from pydantic import BaseModel

class ResearchRequest(BaseModel):
    """
    Trader -> Researcher 로 전달되는 리서치 요청 메시지
    """
    stock_code: Annotated[str, "조사할 개별 종목 코드"]
    stock_name: Annotated[str, "조사할 개별 종목 이름"]

class DebateResult(BaseModel):
    """
    Bullish/Bearish 리서치 결과
    """
    speaker: Annotated[str, "토론 참여자 이름 (Bullish Analyst / Bearish Analyst)"]
    reason: Annotated[str, "토론에서 나온 주요 근거"]
    confidence: Annotated[float, "토론 결과에 대한 신뢰도 (0.0 ~ 1.0)"]

class ResearchResultsResponse(BaseModel):
    stock_code: Annotated[str, "조사했던 개별 종목 코드"]
    debate_history: Annotated[List[DebateResult], "Bullish/Bearish 토론 결과 리스트"]
    summarized: Annotated[str, "토론 결과를 요약한 인사이트"]

class RiskAssessmentRequest(BaseModel):
    """
    Trader -> Risk Manager 로 전달되는 리스크 평가 요청 메시지
    """
    research_results: Annotated[List[ResearchResultsResponse], "리서치 팀이 조사한 종목별 리서치 결과 리스트"]

class TradingDecision(BaseModel):
    action: Annotated[str, "매수 또는 매도 결정"]
    reason: Annotated[str, "매수/매도 결정을 내린 근거"]
    confidence: Annotated[float, "결정에 대한 신뢰도 (0.0 ~ 1.0)"]
    stock_code: Annotated[str, "주식 종목 코드"]

class RiskAssessmentResult(BaseModel):
    "개별 RiskManager들이 Manager에게 전달하는 리스크 평가 결과"
    trading_decision: Annotated[List[TradingDecision], "최종 매수/매도 결정"]