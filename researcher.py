from tavily import TavilyClient
from dotenv import load_dotenv
import os 

load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def researcher_node(state):
    topic = state['topic']

    results = tavily_client.search(query=topic)
    combined_text = ''
    for item in results['results'][:3]:
        combined_text += f"{item['title']}\n{item['url']}\n{item['content']}\n\n---\n\n"

    state['search_results'] = combined_text
    return state

if __name__ == "__main__":
    test_state = {"topic": "What is LangGraph", "search_results": "", "summary": "", "report": ""}
    output = researcher_node(test_state)
    print(output)