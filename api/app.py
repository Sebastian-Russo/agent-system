"""
Personal Assistant Agent - Flask API
"""
import sys
import os
sys.path.insert(0, '.')

from flask import Flask, request, jsonify
from src.agent.agent import Agent

app = Flask(__name__)
agent = Agent()
print("✓ Agent API ready!")


@app.route('/ask', methods=['POST'])
def ask():
    """
    Send a message to the agent
    Body: {"message": "What's the weather in Tokyo?"}
    """
    data = request.get_json()

    if not data or 'message' not in data:
        return jsonify({"error": "Missing 'message' field"}), 400

    result = agent.run(data['message'])

    return jsonify({
        "message": data['message'],
        "answer": result['answer'],
        "steps": result['steps']
    })


@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "ok",
        "tools": [t['name'] for t in agent._call_claude.__code__.co_consts if isinstance(t, str)]
    })


@app.route('/tools', methods=['GET'])
def tools():
    """List available tools"""
    from src.agent.agent import TOOLS
    return jsonify({
        "tools": [
            {"name": t["name"], "description": t["description"]}
            for t in TOOLS
        ]
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)
