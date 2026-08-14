"""Program Intelligence Copilot - portfolio V1.

A small Streamlit application that turns an unstructured TPM update into
structured program intelligence using an LLM. The model is optional: when
no API key is configured, the app provides a transparent demo mode so the
portfolio remains runnable without credentials.
"""

import json
import os
from typing import Any

import streamlit as st

try:
    from groq import Groq
except ImportError:  # pragma: no cover - handled by requirements
    Groq = None


st.set_page_config(
    page_title="Program Intelligence Copilot",
    page_icon="🧭",
    layout="wide",
)

DEFAULT_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

SYSTEM_PROMPT = """You are a Technical Program Management intelligence assistant.
Analyze only the information provided by the user. Do not invent facts.
Separate stated facts from reasonable inference. If an important relationship
is unknown, call it out as an uncertainty.

Return valid JSON with exactly these keys:
executive_summary, program_health, risks, blockers, dependencies,
recommended_next_actions.

program_health must contain status (Green, Amber, or Red) and reason.
risks, blockers, dependencies, and recommended_next_actions must be arrays.
Each risk should contain risk, impact, mitigation. Each dependency should
contain dependency and why_it_matters. Actions should be concise and ordered.
"""

DEMO_RESULT = {
    "executive_summary": "Development is 80% complete with four weeks remaining. The mandatory security review has not started and requires two weeks, while a vendor API issue may take up to one week to resolve. The remaining runway is therefore compressed with limited contingency.",
    "program_health": {
        "status": "Amber",
        "reason": "The security review consumes half of the remaining runway, leaving limited time for the vendor fix, remaining development, integration, testing, and retesting."
    },
    "risks": [
        {
            "risk": "Security review has not started",
            "impact": "Could delay go-live if the review cannot complete within the remaining runway.",
            "mitigation": "Kick off the review immediately and confirm the lead time and review prerequisites."
        },
        {
            "risk": "Vendor API issue remains unresolved",
            "impact": "May consume up to one week and could affect downstream testing.",
            "mitigation": "Obtain a firm vendor resolution date and confirm whether it blocks security testing."
        }
    ],
    "blockers": [
        "Security review is not yet scheduled.",
        "Vendor API issue is unresolved."
    ],
    "dependencies": [
        {"dependency": "Security team", "why_it_matters": "Two-week mandatory review lead time."},
        {"dependency": "Vendor", "why_it_matters": "API resolution may take up to one week."},
        {"dependency": "Development team", "why_it_matters": "20% of development remains."}
    ],
    "recommended_next_actions": [
        "Start the security review immediately.",
        "Get a committed vendor resolution date.",
        "Confirm whether the vendor fix and security review can run in parallel.",
        "Set an early go/no-go checkpoint for the launch date."
    ]
}


def analyze_with_groq(update: str) -> dict[str, Any]:
    """Call Groq and parse the structured response."""
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

    content = response.choices[0].message.content
    result = json.loads(content)
    validate_result(result)
    return result


def validate_result(result: dict[str, Any]) -> None:
    """Perform lightweight schema validation before displaying model output."""
    required = {
        "executive_summary",
        "program_health",
        "risks",
        "blockers",
        "dependencies",
        "recommended_next_actions",
    }
    missing = required - result.keys()
    if missing:
        raise ValueError(f"Model response is missing fields: {', '.join(sorted(missing))}")

    status = result["program_health"].get("status")
    if status not in {"Green", "Amber", "Red"}:
        raise ValueError("Program health status must be Green, Amber, or Red")


def render_result(result: dict[str, Any]) -> None:
    health = result["program_health"]
    status = health["status"]

    st.subheader("Program Health")
    st.metric("Status", status, health.get("reason", ""))

    st.subheader("Executive Summary")
    st.write(result["executive_summary"])

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


st.title("🧭 Program Intelligence Copilot")
st.caption("AI-assisted program analysis for Technical Program Managers")

with st.expander("What this demonstrates", expanded=False):
    st.write(
        "This portfolio application converts an unstructured program update into "
        "health, risks, blockers, dependencies, and recommended actions. "
        "The TPM remains accountable for validating the analysis and making decisions."
    )

sample = """Development is 80% complete with 4 weeks remaining before go-live.
The security review has not started and requires 2 weeks.
A vendor API issue is unresolved and may take up to 1 week to fix.
The team still needs to complete final development and integration testing."""

update = st.text_area(
    "Paste a program update",
    value=sample,
    height=180,
    max_chars=12000,
    help="Use synthetic or non-confidential information for this portfolio demo.",
)

col_a, col_b = st.columns([1, 4])
with col_a:
    analyze = st.button("Analyze Program", type="primary", use_container_width=True)

if analyze:
    if not update.strip():
        st.warning("Enter a program update first.")
    else:
        with st.spinner("Analyzing program signals..."):
            try:
                result = analyze_with_groq(update)
                st.success("AI analysis complete")
            except Exception as exc:
                # Deliberately avoid displaying raw provider errors or credentials.
                st.info("AI provider is not configured or returned an invalid response. Showing the deterministic demo analysis instead.")
                result = DEMO_RESULT
        render_result(result)

st.divider()
st.caption("Portfolio V1 • Synthetic examples • Human review required for consequential decisions")
