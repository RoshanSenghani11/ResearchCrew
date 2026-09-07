import streamlit as st
import os
from graph import app as research_app

st.set_page_config(
    page_title = "ResearchCrew",
    page_icon = "🔍"
) 

st.title("ResearchCrew")

topic = st.text_input("What you got today?", max_chars = 200)

if st.button("Search"):
    if topic:
        state = {"topic": topic, "search_results": "", "summary": "", "report": ""}
        with st.spinner("Searching your topic..."):
            result = research_app.invoke(state)
        st.session_state["report"] = result["report"]
    else:
        st.warning("Input box is empty, please! mention what you want to search?")

if "report" in st.session_state:
    st.markdown(st.session_state["report"])
    st.download_button(
        label="Download reports",
        data=st.session_state["report"],
        file_name="research_report.md",
        mime="text/markdown"
    )
    clean_text = st.session_state["report"].replace("**", "").replace("##", "").replace("#", "")
    st.download_button(
        label="Download as plain text",
        data=clean_text,
        file_name="research_report.txt",
        mime="text/plain",
    )