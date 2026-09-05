# ResearchCrew — Progress Notes (Updated)

**Project:** Multi-agent AI research assistant (LangGraph + Groq + Tavily)
**Status:** ✅ Core CLI pipeline complete — takes any user topic, runs 3 agents, saves report to file

---

## Stack
- Python
- LangGraph (agent orchestration)
- LangChain-Groq (LLM calls — model: `openai/gpt-oss-20b`)
- Tavily (web search)
- python-dotenv (API key management)

## Architecture
```
User input (topic)
      ↓
Researcher → Summarizer → Writer
      ↓
Printed to terminal + saved to report.md
```

- **State**: shared dict (`ResearchState` TypedDict) with fields `topic`, `search_results`, `summary`, `report`
- **Researcher node**: takes `topic`, searches Tavily, extracts top 3 results (title/url/content), joins into a string → `search_results`
- **Summarizer node**: takes `search_results`, prompts Groq LLM for a 5-bullet plain-language summary → `summary`
- **Writer node**: takes `topic` + `summary`, prompts Groq LLM for a structured report (title, intro, body sections, conclusion) → `report`
- **Graph**: `StateGraph` wiring the 3 nodes linearly — entry point `researcher` → `summarizer` → `writer` → `END`

## Files
| File | Purpose |
|---|---|
| `state.py` | Defines `ResearchState` TypedDict |
| `researcher.py` | Researcher node + Tavily client (has its own isolated test block) |
| `summarizer.py` | Summarizer node + Groq LLM client (has its own isolated test block) |
| `writer.py` | Writer node (reuses same LLM pattern) |
| `graph.py` | Wires all 3 nodes into a runnable app; **main entry point** — takes user input, runs pipeline, prints + saves report |
| `report.md` | Output file — gets **overwritten** each run (single-file, no history, by design for now) |
| `.env` | Holds `GROQ_API_KEY` and `TAVILY_API_KEY` (not committed to git) |
| `requirements.txt` | Pinned dependency versions |
| `runtime.txt` | `python-3.11` — forces correct Python version for Streamlit Cloud later |

## Key concepts learned
- **State** = shared dict passed between agents
- **Node** = one function = one agent, takes state in, returns updated state
- **Edge** = defines execution order (`add_edge("from", "to")`)
- `set_entry_point("name")` — only ONE argument, marks the first node (different from `add_edge`, which connects two nodes)
- `workflow.compile()` — turns the graph blueprint into a runnable `app`
- `app.invoke(state)` — actually runs the full pipeline
- Writing files: `open("file.md", "w", encoding="utf-8")` + `with` block, `"w"` = overwrite mode

## Verified working
- Ran end-to-end on multiple different topics ("What is LangGraph", "Tell me about AI agents", and a book-summary style topic) — each produced a clean, correctly structured report with no leftover data from previous runs.
- Confirmed `report.md` saves correctly and renders properly as markdown in VS Code.

---

## Next steps
1. **Now:** Git/GitHub setup — repo, `.gitignore`, README, pinned `requirements.txt`, commit history
2. **Later:** Wrap in Streamlit (same deployment pattern as DocMind)
3. **Optional future improvement:** dynamic filenames (topic + timestamp) if report history becomes useful — intentionally skipped for now to keep things simple

## Deployment reminders (from DocMind lessons)
- Pin **exact** versions in `requirements.txt` (`pip freeze > requirements.txt`)
- `runtime.txt` → `python-3.11` (already created)
- Watch for similar version conflicts DocMind hit (httpx/groq, transformers/torch) if new packages get added later