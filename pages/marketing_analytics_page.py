import json
import html
import sys
from pathlib import Path

import streamlit as st

#Fixing import problems
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from agents.marketing_analytics.marketing_analyst_agent import marketingAnalyticsAgent


st.set_page_config(
    page_title="Marketing Analytics AI Agent",
    layout="centered",
)
st.title("Marketing Analytics AI Agent")

with st.form("marketing_report_form"):
    marketing_data_path = st.text_input(
        "Marketing data path",
        placeholder="data/marketing/shopee_ads/overall_data/your_report.csv",
    )
    retriever = st.selectbox(
        "Retriever",
        options=["term", "embedding"],
        index=0,
    )
    generate_report = st.form_submit_button("Generate marketing report")

if generate_report:
    for key in ("relevant_observations", "relevant_query", "relevant_decisions"):
        st.session_state.pop(key, None)

    if not marketing_data_path.strip():
        st.error("Enter the path to a marketing data CSV file.")
    else:
        marketing_analytics_agent = marketingAnalyticsAgent()
        try:
            solution, relevant_observations, relevant_query = (
                marketing_analytics_agent.analyse_marketing_performance_pipeline(
                    marketing_data_path=marketing_data_path.strip(),
                    retriever=retriever,
                )
            )
            if isinstance(solution, str):
                solution = json.loads(solution)
            relevant_decisions = solution.get("relevant_decisions", [])
            if not isinstance(relevant_decisions, list):
                raise ValueError("The solution must contain a list of relevant_decisions.")

            st.session_state["relevant_observations"] = relevant_observations
            st.session_state["relevant_query"] = relevant_query
            st.session_state["relevant_decisions"] = relevant_decisions
        except Exception as error:
            st.error(f"Could not generate the marketing report: {error}")

if st.session_state.get("relevant_observations"):
    st.subheader("Relevant Observations")
    observations = st.session_state["relevant_observations"]
    for row_start in range(0, len(observations), 3):
        cards = []
        for index in range(row_start, min(row_start + 3, len(observations))):
            safe_observation = html.escape(str(observations[index])).replace(
                "\n", "<br>"
            )
            cards.append(
                f"""
                <div style="box-sizing: border-box; height: 100%;
                            border: 1px solid; border-radius: 0.5rem;
                            padding: 1rem;">
                    <strong>Observation {index + 1}</strong><br><br>{safe_observation}
                </div>
                """
            )
        st.html(
            "<div style='display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); "
            "align-items: stretch; gap: 0.75rem; margin-bottom: 0.75rem;'>"
            + "".join(cards)
            + "</div>"
        )

if st.session_state.get("relevant_query"):
    st.subheader("What to look for?")
    with st.container(border=True):
        st.markdown("**Look for**")
        st.write(st.session_state["relevant_query"])

if st.session_state.get("relevant_decisions"):
    st.subheader("Next steps")
    for index, decision in enumerate(
        st.session_state["relevant_decisions"],
        start=1,
    ):
        safe_decision = html.escape(str(decision)).replace("\n", "<br>")
        st.markdown(
            f"""
            <div style="background-color: #c8e6c9; border: 1px solid #dedede;
                        border-radius: 0.5rem; padding: 1rem; margin-bottom: 0.75rem;
                        color: #111111;">
                <strong>Step {index}</strong><br><br>{safe_decision}
            </div>
            """,
            unsafe_allow_html=True,
        )

