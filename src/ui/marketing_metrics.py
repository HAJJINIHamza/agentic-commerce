import streamlit as st

def metric_card(
    title,
    value,
    subtitle=None,
    delta=None,
    delta_type="neutral",
):
    delta_class = f"delta-{delta_type}" if delta else ""

    delta_html = ""
    if delta:
        delta_html = f"""
        <div class="metric-delta {delta_class}">
            {delta}
        </div>
        """

    subtitle_html = ""
    if subtitle:
        subtitle_html = f"""
        <div class="metric-subtitle">
            {subtitle}
        </div>
        """

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
            {subtitle_html}
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

def metric_section(title, description=None):
    description_html = ""

    if description:
        description_html = f"""
        <div class="section-description">
            {description}
        </div>
        """

    st.markdown(
        f"""
        <div class="metric-section">
            <div class="section-title">{title}</div>
            {description_html}
        """,
        unsafe_allow_html=True,
    )
