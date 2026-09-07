from langchain_groq import ChatGroq 
from dotenv import load_dotenv
import os 

load_dotenv()

llm = ChatGroq(
    api_key = os.getenv("GROQ_API_KEY"),
    model = "openai/gpt-oss-20b"
)

def writer_node(state):
    topic = state["topic"]
    summary = state["summary"]

    prompt = f"""
    {topic},
    it is a report not a summary, you have to create a structured report on the given topic, for reference I am sharing you the summary -> {summary}

    Rules:
    - Use simple, everyday language throughout — avoid jargon and technical terms
    - If a technical term is necessary, explain what it means in plain words right after
    - Keep sentences short and clear
    - Write as if explaining to someone who is smart but has no background in this topic

    report should be in order like first - title, then a short intro, then a couple of body sections and at the very end a brief conclusion. Make this as simple as possible.

    Title -> Short Intro -> Body Section -> Brief Conclusion
    
    Format the report using proper Markdown, with these sections in this order:
    1. An engaging, descriptive title (not literally the word "Title")
    2. A short introduction section — give it a natural heading like "Overview" or "What You Need to Know" (not literally "Short Intro")
    3. A few body sections — each with a specific, relevant heading based on what that section covers (not generic labels like "Body Section 1")
    4. A closing section — give it a natural heading like "Wrapping Up" or "Key Takeaway" (not literally "Brief Conclusion")

    Use "# " for the main title, "## " for each section heading, "**bold**" for key terms, and "- " for bullets where useful.
    """

    response = llm.invoke(prompt)

    state["report"] = response.content
    return state

if __name__ == "__main__":
    test_state = {"topic": "What is LangGraph", "search_results": "What is LangGraph?\nhttps://www.ibm.com/think/topics/langgraph\nLangGraph, created by LangChain, is an open source AI agent framework designed to build, deploy and manage complex generative AI agent workflows. It provides a set of tools and libraries that enable users to create, run and optimize large language models (LLMs) in a scalable and efficient manner. At its core, LangGraph uses the power of graph-based architectures to model and manage the intricate relationships between various components of an AI agent workflow. [...] Agent systems: LangGraph provides a framework for building agent-based systems, which can be used in applications such as robotics, autonomous vehicles or video games.\n\nLLM applications: By using LangGraph’s capabilities, developers can build more sophisticated AI models that learn and improve over time. Norwegian Cruise Line uses LangGraph to compile, construct and refine guest-facing AI solutions. This capability allows for improved and personalized guest experiences. [...] LangGraph illuminates the processes within an AI workflow, allowing full transparency of the agent’s state. Within LangGraph, the “state” feature serves as a memory bank that records and tracks all the valuable information processed by the AI system. It’s similar to a digital notebook where the system captures and updates data as it moves through various stages of a workflow or graph analysis.\n\n---\n\nWhat is LangGraph\nhttps://www.geeksforgeeks.org/machine-learning/what-is-langgraph\ngeeksforgeeks\n\nsearch icon\n\n Interview Prep\n\n DSA\n Practice Problems\n C\n C++\n Java\n Python\n JavaScript\n Data Science\n Machine Learning\n Courses\n Linux\n DevOps\n\n# What is LangGraph\n\nLast Updated : 14 Apr, 2026\n\nLangGraph is an open-source framework from LangChain designed to build and manage AI agent workflows using graph-based structures. It allows developers to define workflows as nodes and edges, making complex agent interactions more structured, scalable and easier to control. [...] langgraph: Framework for building graph-based AI workflows.\n langchain: Popular toolkit for LLM-powered AI applications.\n google-generativeai: Google’s API for Generative AI (Gemini models).\n\n Python  ````\n! pip install langgraph langchain google - generativeai\n```` \n\n### Step 2: Setup Gemini API [...] ## Building a Simple Chatbot with LangGraph\n\nLangGraph makes it easy to build structured, stateful applications like chatbots. In this example we’ll learn how to create a basic chatbot that can classify user input as either a greet, search query and respond accordingly.\n\n### Step 1: Install the Dependencies\n\nInstalls the required dependencies,\n\n---\n\nFoundation: Introduction to LangGraph - Python\nhttps://academy.langchain.com/courses/intro-to-langgraph\nNo. LangGraph is an orchestration framework for complex agentic systems and is more low-level and controllable than LangChain agents. On the other hand, LangChain provides a standard interface to interact with models and other components, useful for straight-forward chains and retrieval flows.\n How is LangGraph different from other agent frameworks? [...] Yes. LangGraph is an MIT-licensed open-source library and is free to use.\n What is LangSmith Deployment?  \n\n  LangSmith Deployment helps you ship your agent in one click, using scalable infrastructure built for long-running tasks.\n\n## Ready to start shipping reliable agents faster?\n\nOur platform provides tools for every step of the agent development lifecycle — built to unlock powerful AI in production.\n\nContact Sales\n\n## Learn with the community [...] Other agentic frameworks can work for simple, generic tasks but fall short for complex tasks bespoke to a company’s needs. LangGraph provides a more expressive framework to handle companies’ unique tasks without restricting users to a single black-box cognitive architecture.\n Does LangGraph impact the performance of my app?  \n\n  LangGraph will not add any overhead to your code and is specifically designed with streaming workflows in mind.\n Is LangGraph open source? Is it free?\n\n---\n\n", "summary": "- **LangGraph is an open‑source tool from LangChain** that lets developers build AI agent workflows using a graph‑based model (nodes and edges).  \n- It is designed for **complex, scalable tasks** such as robotics, autonomous vehicles, or advanced chatbots, and works with any large‑language model (LLM).  \n- The framework keeps a **transparent “state”** that records all data the agent processes, acting like a digital notebook that updates as the workflow runs.  \n- LangGraph adds **no extra performance cost** and is free under an MIT license, making it easy to ship long‑running agents.  \n- Companies use it for real‑world applications—for example, Norwegian Cruise Line builds guest‑facing AI services with LangGraph to improve personalized experiences.", "report": ""}
    output = writer_node(test_state)
    print(output)