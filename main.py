import asyncio
import logging
import os

from agents.architect import Architect
from agents.clean_coder import CleanCoder
from agents.coder import Coder
from agents.messages import StartAnalysisChangelistRequest
from agents.technical_leader import TechnicalLeader
from utils import tools

from agent_framework import (
    WorkflowBuilder,
    WorkflowOutputEvent,
)
from agent_framework.devui import serve
from agent_framework.openai import OpenAIChatClient
from dotenv import load_dotenv

load_dotenv()


def main():
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logger = logging.getLogger(__name__)

    chat_client = OpenAIChatClient(
        model_id=os.getenv("OPENAI_MODEL", "qwen3:4b"),
        base_url=os.getenv("OPENAI_BASE_URL", "http://localhost:11434/v1/"),
        api_key=os.getenv("OPENAI_API_KEY", "dummy"),
    )

    workflow = (
        WorkflowBuilder(
            name="",
            description="",
        )
        .set_start_executor(start_node)
        .build()
    )

    entities = [workflow]

    logger.info("Starting DevUI on http://localhost:8090")
    logger.info("Entities available:")

    serve(entities=entities, port=8090, auto_open=True)

if __name__ == "__main__":
    main()