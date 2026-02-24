# Outputs

```bash
$ python3 src/agent/interactive.py
```
============================================================
PERSONAL ASSISTANT AGENT
============================================================

I'm your personal assistant! I can:
  🔢 Do math and calculations
  🌤️  Check the weather anywhere
  🔍 Search the web
  📝 Save and manage notes
  🕐 Tell you the date and time

Type 'quit' to exit
------------------------------------------------------------

🤖 You: What time is it?

============================================================
Agent received: What time is it?
============================================================

--- Step 1 ---
  🔧 Using tool: get_datetime
     Input: {}
     Result: {"date": "2026-02-24", "time": "01:30:41", "day": "Tuesday", "full": "Tuesday, February 24, 2026 at 01:30 AM"}

--- Step 2 ---

--- Final Answer ---
It's currently 1:30 AM on Tuesday, February 24, 2026.

📎 Assistant: It's currently 1:30 AM on Tuesday, February 24, 2026.
============================================================

🤖 You: What's the weather in Tokyo?

============================================================
Agent received: What's the weather in Tokyo?
============================================================

--- Step 1 ---
  🔧 Using tool: get_weather
     Input: {"location": "Tokyo"}
     Result: {"location": "Tokyo, Japan", "temperature_c": 16.3, "temperature_f": 61.3, "windspeed_kmh": 5.4, "description": "Partly cloudy"}

--- Step 2 ---

--- Final Answer ---
The current weather in Tokyo, Japan is:
- Temperature: 16.3°C (61.3°F)
- Conditions: Partly cloudy
- Wind speed: 5.4 km/h

It's a pleasant mild day with partly cloudy skies!

📎 Assistant: The current weather in Tokyo, Japan is:
- Temperature: 16.3°C (61.3°F)
- Conditions: Partly cloudy
- Wind speed: 5.4 km/h

It's a pleasant mild day with partly cloudy skies!
============================================================

🤖 You: What's 20% tip on a $85 dinner?

============================================================
Agent received: What's 20% tip on a $85 dinner?
============================================================

--- Step 1 ---
  🔧 Using tool: calculator
     Input: {"expression": "85 * 0.20"}
     Result: {"result": 17.0}

--- Step 2 ---

--- Final Answer ---
A 20% tip on an $85 dinner would be $17.00.

📎 Assistant: A 20% tip on an $85 dinner would be $17.00.
============================================================

🤖 You: What's the weather in Paris, convert the temperature to Fahrenheit, and save the result to my notes

============================================================
Agent received: What's the weather in Paris, convert the temperature to Fahrenheit, and save the result to my notes
============================================================

--- Step 1 ---
  🔧 Using tool: get_weather
     Input: {"location": "Paris"}
     Result: {"location": "Paris, France", "temperature_c": 12.5, "temperature_f": 54.5, "windspeed_kmh": 4.8, "description": "Overcast"}

--- Step 2 ---
  🔧 Using tool: calculator
     Input: {"expression": "(12.5 * 9/5) + 32"}
     Result: {"result": 54.5}

--- Step 3 ---
  🔧 Using tool: save_note
     Input: {"title": "Paris Weather", "content": "Weather in Paris, France:\n- Temperature: 12.5\u00b0C (54.5\u00b0F)\n- Wind Speed: 4.8 km/h\n- Conditions: Overcast"}
     Result: {"saved": "Paris Weather"}

--- Step 4 ---

--- Final Answer ---
Done! Here's what I found and saved:

**Current weather in Paris, France:**
- Temperature: 12.5°C (54.5°F)
- Wind Speed: 4.8 km/h
- Conditions: Overcast

The weather information has been saved to your notes under the title "Paris Weather" for future reference.

📎 Assistant: Done! Here's what I found and saved:

**Current weather in Paris, France:**
- Temperature: 12.5°C (54.5°F)
- Wind Speed: 4.8 km/h
- Conditions: Overcast

The weather information has been saved to your notes under the title "Paris Weather" for future reference.
============================================================

🤖 You:
