from langgraph.graph import StateGraph, END
from state import ResearchState
from researcher import researcher_node
from summarizer import summarizer_node
from writer import writer_node

workflow = StateGraph(ResearchState)

workflow.add_node("researcher", researcher_node)
workflow.add_node("summarizer", summarizer_node)
workflow.add_node("writer", writer_node)

workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "summarizer")
workflow.add_edge("summarizer", "writer")
workflow.add_edge("writer", END)

app = workflow.compile()

if __name__ == "__main__":
    user_input = input("What is today's topic?\n")
    test_state = {"topic": user_input, "search_results": "", "summary": "", "report": ""}
    final_output = app.invoke(test_state)
    print(final_output["report"])

    with open('report.md', 'w', encoding='utf-8') as f:
        f.write(final_output['report'])


