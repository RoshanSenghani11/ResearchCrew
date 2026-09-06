import streamlit as st
import os
from graph import app as research_app

st.title("ResearchCrew")

topic = st.text_input("What you got today?")

if st.button("Search"):
    state = {"topic": topic, "search_results": "", "summary": "", "report": ""}
    result = research_app.invoke(state)
    st.markdown(result["report"])