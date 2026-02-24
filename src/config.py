"""
Agent configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = "claude-sonnet-4-20250514"
MAX_AGENT_STEPS = 10  # Safety limit so the agent can't loop forever
