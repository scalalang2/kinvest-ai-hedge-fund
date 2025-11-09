from pydantic import BaseModel

class StartTradingRequest(BaseModel):
    name: str

class ResearchRequest(BaseModel):
    pass

class ResearchResultsResponse(BaseModel):
    pass

class RiskAssessmentRequest(BaseModel):
    pass

class RiskAssessmentResult(BaseModel):
    pass