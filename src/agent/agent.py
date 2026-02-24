"""
Agent - The ReAct Loop
The brain that decides what to do, uses tools, and observes results

ANALOGY - THE OFFICE WORKER:
Imagine an office worker at a desk with tools around them:
- Calculator on the desk
- Clock on the wall
- Notebook for notes
- Phone to search the internet
- Window to check the weather

You walk in and say "What's 20% tip on a $85 dinner, and
save that to my notes?"

The worker THINKS: "I need to calculate 20% of 85, then save it."
The worker ACTS:   Picks up calculator, types 85 * 0.20
The worker SEES:   Calculator shows 17.0
The worker THINKS: "Got $17. Now I need to save this to notes."
The worker ACTS:   Opens notebook, writes "Tip: $17.00"
The worker SEES:   Note saved successfully
The worker THINKS: "Done! I have everything to answer."
The worker ANSWERS: "A 20% tip on $85 is $17.00. I've saved that
                     to your notes."

That's the ReAct loop: Think → Act → Observe → Repeat → Answer

The LLM (Claude) is the worker's brain.
The tools are the objects on the desk.
The loop continues until the worker has enough info to answer.
"""
import json
import requests
from src.config import ANTHROPIC_API_KEY, ANTHROPIC_MODEL, MAX_AGENT_STEPS
from src.tools.calculator import calculator
from src.tools.datetime_tool import get_datetime
from src.tools.notes import save_note, read_note, list_notes, delete_note
from src.tools.weather import get_weather
from src.tools.web_search import web_search


# ============================================================
# TOOL REGISTRY
# ============================================================
# The tool registry tells the agent what tools exist and how to use them.
# Each tool has:
# - name: what the agent calls it
# - description: when to use it (the agent reads this to decide)
# - parameters: what inputs it needs
# - function: the actual Python function to call
#
# ANALOGY: A manual on the worker's desk listing every tool,
# what it does, and how to use it. The worker reads this manual
# to figure out which tool to grab.

TOOLS = [
    {
        "name": "calculator",
        "description": "Evaluate math expressions. Use for any arithmetic, percentages, conversions, or calculations.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Math expression to evaluate, e.g. '(85 * 0.20)' or '((18 * 9) / 5) + 32'"
                }
            },
            "required": ["expression"]
        }
    },
    {
        "name": "get_datetime",
        "description": "Get the current date, time, and day of the week. Use when the user asks about today's date, current time, or what day it is.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "get_weather",
        "description": "Get current weather for any location. Use when the user asks about weather, temperature, or conditions in a place.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City or location name, e.g. 'Paris' or 'New York'"
                }
            },
            "required": ["location"]
        }
    },
    {
        "name": "web_search",
        "description": "Search the web for current information. Use when you need facts, news, or information you don't know.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "save_note",
        "description": "Save a note with a title and content. Use when the user asks you to remember, save, or write something down.",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Title or name for the note"
                },
                "content": {
                    "type": "string",
                    "description": "Content of the note"
                }
            },
            "required": ["title", "content"]
        }
    },
    {
        "name": "read_note",
        "description": "Read a previously saved note. Use when the user asks to see or recall a note.",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Title of the note to read"
                }
            },
            "required": ["title"]
        }
    },
    {
        "name": "list_notes",
        "description": "List all saved notes. Use when the user asks what notes they have.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "delete_note",
        "description": "Delete a saved note. Use when the user asks to remove or delete a note.",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Title of the note to delete"
                }
            },
            "required": ["title"]
        }
    }
]

# Map tool names to their Python functions
TOOL_FUNCTIONS = {
    "calculator": lambda args: calculator(args["expression"]),
    "get_datetime": lambda args: get_datetime(),
    "get_weather": lambda args: get_weather(args["location"]),
    "web_search": lambda args: web_search(args["query"]),
    "save_note": lambda args: save_note(args["title"], args["content"]),
    "read_note": lambda args: read_note(args["title"]),
    "list_notes": lambda args: list_notes(),
    "delete_note": lambda args: delete_note(args["title"]),
}


# ============================================================
# THE AGENT
# ============================================================
class Agent:
    """
    ReAct Agent - Reason and Act in a loop

    HOW THE LOOP WORKS:

    1. Send the user's question + tool descriptions to Claude
    2. Claude either:
       a) Calls a tool → we execute it and send the result back
       b) Gives a final answer → we return it to the user
    3. If a tool was called, go back to step 2 with the result
    4. Repeat until Claude gives a final answer or we hit the step limit

    ANALOGY:
    It's like texting a really smart friend who has access to
    a bunch of apps. You text them a question. They might text
    back "let me check the weather app..." then "ok now let me
    do some math..." then finally give you the answer. Each
    text back and forth is one step in the loop.
    """

    def __init__(self):
        self.system_prompt = """You are a helpful personal assistant with access to tools.
Use tools when you need to look up information, do calculations,
check the weather, search the web, or manage notes.

Guidelines:
- Use tools when they would help answer the question accurately
- Don't use tools if you can answer from your own knowledge
- For math, always use the calculator instead of doing mental math
- Be concise but helpful in your final answers
- If a tool returns an error, tell the user what went wrong"""

    def _call_claude(self, messages):
        """
        Send messages to Claude with tool definitions

        ANALOGY: Talking to the worker's brain.
        We describe all available tools and the conversation so far.
        The brain either says "I need to use tool X" or "Here's my answer."
        """
        # Convert our tool format to Anthropic's tool format
        anthropic_tools = [
            {
                "name": tool["name"],
                "description": tool["description"],
                "input_schema": tool["parameters"]
            }
            for tool in TOOLS
        ]

        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json"
            },
            json={
                "model": ANTHROPIC_MODEL,
                "max_tokens": 1024,
                "system": self.system_prompt,
                "tools": anthropic_tools,
                "messages": messages
            },
            timeout=30
        )

        return response.json()

    def _execute_tool(self, tool_name, tool_input):
        """
        Execute a tool and return its result

        ANALOGY: The worker picks up the tool and uses it.
        Calculator → punches in numbers → gets result.
        Weather → looks out the window → sees conditions.
        """
        if tool_name not in TOOL_FUNCTIONS:
            return {"error": f"Unknown tool: {tool_name}"}

        print(f"  🔧 Using tool: {tool_name}")
        print(f"     Input: {json.dumps(tool_input)}")

        result = TOOL_FUNCTIONS[tool_name](tool_input)

        print(f"     Result: {json.dumps(result)}")
        return result

    def run(self, user_message):
        """
        Run the full ReAct loop

        ANALOGY - THE FULL CONVERSATION:
        You: "What's the weather in Tokyo and convert to Fahrenheit?"

        Step 1:
          Brain THINKS: "I need the weather in Tokyo"
          Brain ACTS:   Uses weather tool for "Tokyo"
          Brain SEES:   {"temperature_c": 12, ...}

        Step 2:
          Brain THINKS: "I have the info, let me respond"
          Brain ANSWERS: "It's 12°C (53.6°F) in Tokyo"

        Each step is one round trip to Claude.
        """
        print(f"\n{'='*60}")
        print(f"Agent received: {user_message}")
        print(f"{'='*60}")

        # Start with the user's message
        messages = [{"role": "user", "content": user_message}]

        # Track steps for logging
        steps = []

        for step in range(MAX_AGENT_STEPS):
            print(f"\n--- Step {step + 1} ---")

            # Ask Claude what to do
            response = self._call_claude(messages)

            # Check for errors
            if "error" in response:
                return {
                    "answer": f"API Error: {response['error']['message']}",
                    "steps": steps
                }

            # Check what Claude wants to do
            stop_reason = response.get("stop_reason")

            # If Claude wants to use a tool
            if stop_reason == "tool_use":
                # Claude's response might have text AND tool calls
                # We need to add the full response to messages
                assistant_content = response["content"]
                messages.append({"role": "assistant", "content": assistant_content})

                # Process each tool call in the response
                tool_results = []
                for block in assistant_content:
                    if block["type"] == "tool_use":
                        tool_name = block["name"]
                        tool_input = block["input"]
                        tool_id = block["id"]

                        # Execute the tool
                        result = self._execute_tool(tool_name, tool_input)

                        # Track the step
                        steps.append({
                            "tool": tool_name,
                            "input": tool_input,
                            "result": result
                        })

                        # Format result for Claude
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": tool_id,
                            "content": json.dumps(result)
                        })

                # Send tool results back to Claude
                # ANALOGY: Showing the worker what the tool returned
                # so they can decide what to do next
                messages.append({"role": "user", "content": tool_results})

            # If Claude is done (has a final answer)
            elif stop_reason == "end_turn":
                # Extract the text answer
                answer = ""
                for block in response["content"]:
                    if block["type"] == "text":
                        answer += block["text"]

                print("\n--- Final Answer ---")
                print(answer)

                return {
                    "answer": answer,
                    "steps": steps
                }

        # Hit the step limit
        return {
            "answer": "I ran out of steps trying to answer your question. Please try a simpler request.",
            "steps": steps
        }
