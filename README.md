# ResearchCrew — Progress Notes (Final Update)

**Project:** Multi-agent AI research assistant (LangGraph + Groq + Tavily)
**Status:** ✅ Fully built, deployed live, pushed to GitHub with proper docs

**Live app:** https://researchcrew-2611.streamlit.app/
**Repo:** https://github.com/RoshanSenghani11/ResearchCrew

---

## Stack
- Python
- LangGraph (agent orchestration)
- LangChain-Groq (LLM calls — model: `openai/gpt-oss-20b`)
- Tavily (web search)
- Streamlit (UI)
- python-dotenv (local API key management)

## Architecture
```
User input (topic)
      ↓
Researcher → Summarizer → Writer
      ↓
Displayed in Streamlit + downloadable as .md / .txt
```

- **State**: shared dict (`ResearchState` TypedDict) — fields: `topic`, `search_results`, `summary`, `report`
- **Researcher node**: takes `topic`, searches Tavily, extracts top 3 results (title/url/content) → `search_results`
- **Summarizer node**: takes `search_results`, prompts Groq LLM for a 5-bullet, plain-language summary (explicit "explain like I'm a curious teenager" rule) → `summary`
- **Writer node**: takes `topic` + `summary`, prompts Groq LLM for a structured, markdown-formatted report with natural (non-generic) section headings, plain language throughout → `report`
- **Graph**: `StateGraph` — entry point `researcher` → `summarizer` → `writer` → `END`

## Files
| File | Purpose |
|---|---|
| `state.py` | Defines `ResearchState` TypedDict |
| `researcher.py` | Researcher node + Tavily client (isolated test block) |
| `summarizer.py` | Summarizer node + Groq LLM client, plain-language prompt |
| `writer.py` | Writer node, plain-language + markdown-formatting + natural-heading prompt |
| `graph.py` | Wires all 3 nodes into a runnable app; CLI entry point (user input → pipeline → print + save to `report.md`) |
| `app.py` | Streamlit UI — imports `graph.py`'s compiled app, runs full pipeline on user input |
| `README.md` | Proper project README (description, tech stack, how it works, how to run, live demo link) |
| `.env` | Holds `GROQ_API_KEY` / `TAVILY_API_KEY` locally (gitignored) |
| `requirements.txt` | Pinned dependency versions |
| `runtime.txt` | `python-3.11` — forces correct Python version on Streamlit Cloud |
| `.gitignore` | Excludes `crew/` (venv), `.env`, `__pycache__/`, `*.pyc`, `report.md` |

## Streamlit app features (app.py)
- Title + custom page icon (`st.set_page_config`)
- Text input with `max_chars=200` (basic abuse/cost protection)
- "Search" button triggers pipeline inside `st.spinner(...)` for loading feedback
- Empty-input guard (`st.warning(...)` if topic is blank)
- Report persisted via `st.session_state` (fixes Streamlit's rerun-on-interaction behavior wiping the displayed report when a download button is clicked)
- Two download options: `.md` (keeps markdown formatting) and `.txt` (symbols stripped via `.replace()` for plain-text readability)

## Key concepts learned
- **State** = shared dict passed between agents; **Node** = one function/agent; **Edge** = execution order
- `set_entry_point("name")` (1 arg, marks start) vs `add_edge("from","to")` (2 args, connects nodes)
- `workflow.compile()` → runnable `app`; `app.invoke(state)` → runs the full pipeline
- Writing files: `open(..., "w", encoding="utf-8")` + `with` block
- **Streamlit reruns the entire script on every widget interaction** — `st.session_state` is required to persist data (like a generated report) across those reruns
- `st.spinner(...)` for loading feedback; `st.download_button(...)` for in-browser file downloads
- `st.set_page_config(...)` must be the first Streamlit call, controls tab title/icon

## Key bugs fixed along the way
- Dict key access bugs (`state["topic"]` vs literal strings as keys)
- `+=` vs `=` in loops (was overwriting instead of accumulating)
- Misplaced list slicing (belongs on the loop, not on `state`)
- `response` object vs `response.content` (LLM reply text)
- `set_entry_point` vs `add_edge` confusion; typo `complile()` → `compile()`
- Missing edge caused `"Node not reachable"` graph validation error
- `"topic": "user_input"` (literal string) vs `"topic": user_input` (variable)
- `max_char` vs `max_chars` typo (broke Streamlit Cloud deployment — `TypeError`)
- Download button caused report to visually disappear on click — fixed via `st.session_state` (Streamlit's rerun behavior)
- Wrong git init location (ran in parent folder instead of project folder)
- `.gitignore` mismatch — venv folder is actually named `crew`, not `venv`

## Deployment (Streamlit Community Cloud)
- Repo connected: `RoshanSenghani11/ResearchCrew`, branch `main`, main file `app.py`
- Python version set to 3.11 in Advanced Settings (matches `runtime.txt`)
- API keys added via Streamlit Cloud's **Secrets** manager (TOML format), not `.env` — `os.getenv(...)` still works since Streamlit loads secrets as environment variables
- Fixed one deployment-only bug (`max_char` typo) — app auto-redeployed after git push, confirmed working live

## Verified working
- End-to-end tested on multiple topics (LangGraph, AI agents, book-style content, capital of India, transformer models)
- Plain-language prompt rewrite confirmed working — jargon explained inline, simple sentence structure
- Natural section headings confirmed (e.g., "Overview", "Wrapping Up" instead of generic "Short Intro"/"Brief Conclusion")
- Both download formats confirmed working (`.md` with markdown symbols intact, `.txt` stripped clean)
- Live Streamlit Cloud deployment confirmed fully functional

---

## Completed
- [x] Core 3-agent LangGraph pipeline (CLI)
- [x] Real user input (replacing hardcoded test topic)
- [x] Save report to file
- [x] Streamlit UI wrapper
- [x] Plain-language prompt tuning
- [x] UI polish (spinner, empty-input guard, download buttons, session_state fix, page icon, char limit)
- [x] Git/GitHub setup with proper `.gitignore`
- [x] Deployed live on Streamlit Community Cloud
- [x] Proper README written

## Remaining / optional next steps
- [ ] Show sources/links (URLs) in the final report for authenticity
- [ ] Basic error handling (`try/except`) around Tavily/Groq API calls
- [ ] Update resume with ResearchCrew (accurate tech stack this time)
- [ ] Future: brainstorm one larger, industrial-level project (separate planning session)