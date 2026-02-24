"""
Interactive Agent - test the agent from the command line
"""
import sys
sys.path.insert(0, '.')

from src.agent.agent import Agent

print("=" * 60)
print("PERSONAL ASSISTANT AGENT")
print("=" * 60)
print("\nI'm your personal assistant! I can:")
print("  🔢 Do math and calculations")
print("  🌤️  Check the weather anywhere")
print("  🔍 Search the web")
print("  📝 Save and manage notes")
print("  🕐 Tell you the date and time")
print("\nType 'quit' to exit")
print("-" * 60)

agent = Agent()

while True:
    user_input = input("\n🤖 You: ").strip()

    if not user_input:
        continue
    if user_input.lower() == 'quit':
        print("Goodbye!")
        break

    result = agent.run(user_input)
    print(f"\n📎 Assistant: {result['answer']}")
    print("=" * 60)
