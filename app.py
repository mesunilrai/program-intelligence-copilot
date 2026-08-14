"""Program Intelligence Copilot - portfolio MVP.

Turns an unstructured TPM update into structured program intelligence using
an LLM. The model is optional: without an API key, the app uses an explicit
sample-analysis mode so users are not misled about what was analyzed.
"""

import json
import os
from typing import Any

import streamlit as st

try:
    from groq import Groq
except ImportError:  # pragma: no cover - handled by requirements
    Groq = None


st.set_page_config(page_title="Program Intelligence Copilot", page_icon="🧭", layout="wide")

DEFAULT_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

SYSTEM_PROMPT = """You are a Technical Program Management intelligence assistant.
Analyze only the information provided by the user. Never invent facts.
Separate explicit facts from AI inference. Identify uncertainty when the
information is insufficient to make a conclusion.

Think like a senior TPM. In addition to extracting risks and dependencies,
reason about delivery timing:
- remaining runway and fixed dates
- duration of known activities
- sequencing and parallelism where stated or reasonably inferable
- critical-path pressure
- schedule contingency
- delivery impact if a dependency slips

Do not claim exact critical-path timing unless the input supports it. If timing
cannot be established, say so explicitly.

Return valid JSON with exactly these keys:
executive_summary, program_health, delivery_intelligence, risks, blockers,
dependencies, recommended_next_actions, leadership_attention, facts,
inferences.

program_health must contain status (Green, Amber, or Red) and reason.
delivery_intelligence must contain timeline_assessment, schedule_pressure,
and contingency_assessment.
risk objects must contain risk, impact, mitigation.
dependency objects must contain dependency and why_it_matters.
leadership_attention must contain decision_or_escalation and why_now.
facts and inferences must be arrays of concise strings.
Actions must be concise, ordered, and specific.
"""

DEMO_RESULT = {
    "executive_summary": "Development is 80% complete with four weeks remaining. The mandatory security review has not started and requires two weeks, while a vendor API issue may take up to one week to resolve. The remaining runway is compressed with limited contingency.",
    "program_health": {
        "status": "Amber",
        "reason": "Known work consumes a significant portion of the remaining runway and leaves limited schedule contingency."
    },
    "delivery_intelligence": {
        "timeline_assessment": "Four weeks remain; the two-week security review and up-to-one-week vendor issue consume at least three weeks before considering remaining development and integration testing.",
        "schedule_pressure": "High",
        "contingency_assessment": "Limited. Parallel execution may reduce pressure, but the input does not establish whether the work can fully overlap."
    },
    "risks": [
        {"risk": "Security review has not started", "impact": "Could delay go-live if it cannot complete within the remaining runway.", "mitigation": "Start immediately and confirm prerequisites and lead time."},
        {"risk": "Vendor API issue remains unresolved", "impact": "May consume up to one week and affect downstream testing.", "mitigation": "Obtain a committed resolution date and confirm whether it blocks testing."}
    ],
    "blockers": ["Security review is not yet scheduled.", "Vendor API issue is unresolved."],
    "dependencies": [
        {"dependency": "Security team", "why_it_matters": "Two-week mandatory review lead time."},
        {"dependency": "Vendor", "why_it_matters": "API resolution may take up to one week."}
    ],
    "recommended_next_actions": [
        "Start the security review immediately.",
        "Get a committed vendor resolution date.",
        "Confirm which activities can run in parallel and quantify remaining contingency.",
        "Set an early go/no-go checkpoint for the launch date."
    ],
    "leadership_attention": {
        "decision_or_escalation": "Escalate vendor resolution and confirm whether the launch runway remains achievable.",
        "why_now": "Known work already consumes most of the four-week window."
    },
    "facts": [
        "Development is 80% complete.",
        "Four weeks remain before go-live.",
        "Security review requires two weeks and has not started.",
        "Vendor API resolution may take up to one week."
    ],
    "inferences": [
        "The remaining schedule has limited contingency.",
        "Parallel execution may be required to protect the launch date."
    ]
}


def analyze_with_groq(update: str) -> dict[str, Any]:
    if Groq is None:
        raise RuntimeError("groq package is not installed")
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not configured")

    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        temperature=0.1,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": update[:12000]},
        ],
    )
    result = json.loads(response.choices[0].message.content)
    validate_result(result)
    return result


def validate_result(result: dict[str, Any]) -> None:
    required = {
        "executive_summary", "program_health", "delivery_intelligence", "risks",
        "blockers", "dependencies", "recommended_next_actions",
        "leadership_attention", "facts", "inferences"
    }
    missing = required - result.keys()
    if missing:
        raise ValueError(f"Model response is missing fields: {', '.join(sorted(missing))}")
    if result["program_health"].get("status") not in {"Green", "Amber", "Red"}:
        raise ValueError("Program health status must be Green, Amber, or Red")


def render_result(result: dict[str, Any]) -> None:
    health = result["program_health"]
    delivery = result["delivery_intelligence"]
    leadership = result["leadership_attention"]

    st.subheader("Program Health")
    st.metric("Status", health["status"], health.get("reason", ""))

    st.subheader("Executive Summary")
    st.write(result["executive_summary"])

    st.subheader("🧠 Delivery Intelligence")
    d1, d2, d3 = st.columns(3)
    with d1:
        st.markdown("**Timeline**")
        st.write(delivery.get("timeline_assessment", "Not established"))
    with d2:
        st.markdown("**Schedule Pressure**")
        st.write(delivery.get("schedule_pressure", "Not established"))
    with d3:
        st.markdown("**Contingency**")
        st.write(delivery.get("contingency_assessment", "Not established"))

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("⚠️ Risks")
        for item in result["risks"]:
            if isinstance(item, dict):
                st.markdown(f"**{item.get('risk', 'Risk')}**")
                st.write(f"Impact: {item.get('impact', 'Not specified')}")
                st.write(f"Mitigation: {item.get('mitigation', 'Not specified')}")
            else:
                st.write(item)

        st.subheader("🚧 Blockers")
        for item in result["blockers"]:
            st.write(f"- {item}")

        st.subheader("📌 Facts")
        for item in result["facts"]:
            st.write(f"- {item}")

    with col2:
        st.subheader("🔗 Dependencies")
        for item in result["dependencies"]:
            if isinstance(item, dict):
                st.markdown(f"**{item.get('dependency', 'Dependency')}**")
                st.write(item.get("why_it_matters", ""))
            else:
                st.write(f"- {item}")

        st.subheader("🎯 Recommended Next Actions")
        for index, item in enumerate(result["recommended_next_actions"], start=1):
            st.write(f"{index}. {item}")

        st.subheader("🧩 AI Inferences")
        for item in result["inferences"]:
            st.write(f"- {item}")

    st.subheader("🚨 Leadership Attention")
    st.markdown(f"**Decision / Escalation:** {leadership.get('decision_or_escalation', 'Not identified')}")
    st.write(f"**Why now:** {leadership.get('why_now', 'Not identified')}")


st.title("🧭 Program Intelligence Copilot")
st.caption("AI-assisted program analysis for Technical Program Managers")

with st.expander("What this demonstrates", expanded=False):
    st.write(
        "This portfolio application converts an unstructured program update into "
        "program health, delivery intelligence, risks, blockers, dependencies, "
        "actions, and leadership attention. The TPM remains accountable for validation and decisions."
    )

sample = """Development is 80% complete with 4 weeks remaining before go-live.
The security review has not started and requires 2 weeks.
A vendor API issue is unresolved and may take up to 1 week to fix.
The team still needs to complete final development and integration testing."""

update = st.text_area(
    "Paste a program update", value=sample, height=180, max_chars=12000,
    help="Use synthetic or non-confidential information for this portfolio demo."
)

if st.button("Analyze Program", type="primary", use_container_width=False):
    if not update.strip():
        st.warning("Enter a program update first.")
    else:
        with st.spinner("Analyzing program signals..."):
            try:
                result = analyze_with_groq(update)
                st.success("AI analysis complete")
            except Exception:
                st.info("AI analysis is unavailable. Showing the built-in sample analysis instead. The sample result is not based on the text you entered.")
                result = DEMO_RESULT
        render_result(result)

st.divider()
st.caption("Portfolio MVP • Synthetic examples • Human review required for consequential decisions")
