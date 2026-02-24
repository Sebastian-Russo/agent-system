"""
Calculator Tool
Evaluates math expressions

ANALOGY: A calculator on the agent's desk.
The agent can't do complex math in its head,
so it picks up the calculator when needed.
"""

def calculator(expression):
    """
    Evaluate a math expression

    Input:  "((18 * 9) / 5) + 32"
    Output: {"result": 64.4}
    """
    try:
        # Only allow safe math operations
        allowed = set('0123456789+-*/.() ')
        if not all(c in allowed for c in expression):
            return {"error": f"Invalid characters in expression: {expression}"}

        result = eval(expression)
        return {"result": round(result, 4)}
    except Exception as e:
        return {"error": str(e)}
