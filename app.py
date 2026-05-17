import streamlit as st
import pandas as pd
from openai import OpenAI

# OpenAI Client
client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

# App Title
st.title("AI Prototype: Enterprise Data Governance & Remediation Intelligence Platform")

st.write("""
This prototype explores AI-driven data governance intelligence,
remediation prioritization and human-in-the-loop governance orchestration.
""")

# Upload CSV
uploaded_file = st.file_uploader(
    "Upload Data Governance Dataset",
    type=["csv"]
)

if uploaded_file:

    # Read CSV
    df = pd.read_csv(uploaded_file)

    st.subheader("Uploaded Governance Data")
    st.dataframe(df)

    findings = []

    # Governance analysis
    for index, row in df.iterrows():

        risk_score = 0
        issues = []

        # Missing ownership
        if row["owner_assigned"] == "no":
            risk_score += 30
            issues.append("Missing ownership")

        # Lineage gaps
        if row["lineage_complete"] == "no":
            risk_score += 30
            issues.append("Lineage gap detected")

        # Duplicate datasets
        if row["duplicate_dataset"] == "yes":
            risk_score += 20
            issues.append("Duplicate dataset")

        # Stale controls
        if row["control_review_days"] > 365:
            risk_score += 20
            issues.append("Stale governance controls")

        # Regulatory criticality
        if row["regulatory_criticality"] == "high":
            risk_score += 30
            issues.append("High regulatory exposure")

        # Open remediation issues
        if row["open_issues"] > 3:
            risk_score += 20
            issues.append("Remediation backlog")

        # Automation eligibility
        automation_mode = "Auto-Remediate"

        if row["regulatory_criticality"] == "high":
            automation_mode = "Human Approval Required"

        findings.append({
            "dataset": row["dataset"],
            "risk_score": risk_score,
            "issues": ", ".join(issues),
            "automation_mode": automation_mode
        })

    risk_df = pd.DataFrame(findings)

    # Display findings
    st.subheader("Governance Risk Findings")

    st.dataframe(risk_df)

    # High risk datasets
    high_risk = risk_df[risk_df["risk_score"] >= 60]

    st.subheader("High-Risk Governance Areas")

    st.dataframe(high_risk)

    # Metrics
    st.metric(
        "High-Risk Datasets",
        len(high_risk)
    )

    # Governance score
    avg_score = 100 - int(risk_df["risk_score"].mean())

    st.metric(
        "Governance Health Score",
        f"{avg_score}/100"
    )

    # Chart
    st.bar_chart(
        high_risk.set_index("dataset")["risk_score"]
    )

    # AI Insights
    st.subheader("AI Governance Remediation Insights")

    summary = high_risk.to_string(index=False)

    prompt = f"""
    Analyze the following enterprise data governance findings.

    Identify:
    - ownership weaknesses
    - lineage risks
    - governance gaps
    - remediation bottlenecks
    - operational governance concerns
    - regulatory data risks

    Recommend:
    - remediation priorities
    - governance improvements
    - ownership accountability actions
    - lineage governance enhancements
    - operating model recommendations

    Also identify:
    - which issues can be auto-remediated
    - which issues require human approval

    Findings:
    {summary}
    """

    with st.spinner("Generating AI governance insights..."):

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior enterprise data governance and remediation transformation expert."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        output = response.choices[0].message.content

        st.write(output)
