import asyncio
import logging
import os

from agentlist.messages import StartTradingRequest
from agentlist.trader import Trader
from agentlist.research import Researcher
from agentlist.risk_manager_aggressive import RiskManagerAggressive
from agentlist.risk_manager_conservative import RiskManagerConservative
from agentlist.risk_manager_neutral import RiskManagerNeutral
from agentlist.trading_manager import TradingManager
from kis import create_kis

from agent_framework import (
    Workflow,
    WorkflowBuilder,
    WorkflowOutputEvent,
)
from agent_framework.devui import serve
from agent_framework.openai import OpenAIChatClient
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

def build_workflow():
    args = {
        "model_id": os.getenv("OPENAI_API_MODEL", "gpt-4-turbo"),
        "api_key": os.getenv("OPENAI_API_KEY"),
        **({"base_url": os.getenv("OPENAI_BASE_URL")} if os.getenv("OPENAI_BASE_URL") else {}),
    }

    chat_client = OpenAIChatClient(**args)
    kis = create_kis()

    trader = Trader(model=chat_client)
    researcher = Researcher(model=chat_client)
    risk_manager_aggressive = RiskManagerAggressive(model=chat_client)
    risk_manager_conservative = RiskManagerConservative(model=chat_client)
    risk_manager_neutral = RiskManagerNeutral(model=chat_client)
    manager = TradingManager(model=chat_client)
    
    workflow = (
        WorkflowBuilder(
            name="",
            description="",
        )
        .set_start_executor(trader)
        .add_edge(trader, researcher)
        .add_edge(researcher, trader)
        .add_fan_out_edges(trader, [risk_manager_aggressive, risk_manager_neutral, risk_manager_conservative])
        .add_fan_in_edges([risk_manager_aggressive, risk_manager_neutral, risk_manager_conservative], manager)
        .build()
    )

    return workflow

def run_with_devui(workflow: Workflow):
    entities = [workflow]

    logger.info("Starting DevUI on http://localhost:8090")
    logger.info("Entities available:")

    serve(entities=entities, port=8090, auto_open=True)

async def run(workflow: Workflow):
    start_trading = StartTradingRequest(name="hello")

    async for event in workflow.run_stream(start_trading):
        print(event)

if __name__ == "__main__":
    workflow = build_workflow()
    asyncio.run(run(workflow))