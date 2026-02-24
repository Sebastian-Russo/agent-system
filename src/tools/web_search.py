"""
Web Search Tool
Searches the web using DuckDuckGo (free, no API key needed)

ANALOGY: A phone the agent can use to call the internet
and ask questions. Returns a list of results with titles,
URLs, and snippets.
"""
import requests

def web_search(query):
    """
    Search the web

    Input:  "Python 3.12 release date"
    Output: {"results": [{"title": "...", "url": "...", "snippet": "..."}, ...]}
    """
    try:
        # Using DuckDuckGo instant answer API
        response = requests.get(
            "https://api.duckduckgo.com/",
            params={
                "q": query,
                "format": "json",
                "no_redirect": 1
            },
            timeout=10
        )
        data = response.json()

        results = []

        # Abstract (main answer)
        if data.get("Abstract"):
            results.append({
                "title": data.get("Heading", ""),
                "url": data.get("AbstractURL", ""),
                "snippet": data["Abstract"]
            })

        # Related topics
        for topic in data.get("RelatedTopics", [])[:5]:
            if "Text" in topic:
                results.append({
                    "title": topic.get("Text", "")[:100],
                    "url": topic.get("FirstURL", ""),
                    "snippet": topic.get("Text", "")
                })

        if not results:
            return {"results": [], "note": "No results found. Try different search terms."}

        return {"results": results}
    except requests.RequestException as e:
        return {"error": f"Network error: {str(e)}"}
    except (ValueError, KeyError) as e:
        return {"error": f"Data parsing error: {str(e)}"}
