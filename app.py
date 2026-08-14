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
    "program_health": {"status": "Amber", "reason": "Known work consumes a significant portion of the remaining runway and leaves limited schedule contingency."},
    "delivery_intelligence": {"timeline_assessment": "Four weeks remain; the two-week security review and up-to-one-week vendor issue consume at least three weeks before considering remaining development and integration testing.", "schedule_pressure": "High", "contingency_assessment": "Limited. Parallel execution may reduce pressure, but the input does not establish whether the work can fully overlap."},
    "risks": [
        {"risk": "Security review has not started", "impact": "Could delay go-live if it cannot complete within the remaining runway.", "mitigation": "Start immediately and confirm prerequisites and lead time."},
        {"risk": "Vendor API issue remains unresolved", "impact": "May consume up to one week and affect downstream testing.", "mitigation": "Obtain a committed resolution date and confirm whether it blocks testing."}
    ],
    "blockers": ["Security review is not yet scheduled.", "Vendor API issue is unresolved."],
    "dependencies": [{"dependency": "Security team", "why_it_matters": "Two-week mandatory review lead time."}, {"dependency": "Vendor", "why_it_matters": "API resolution may take up to one week."}],
    "recommended_next_actions": ["Start the security review immediately.", "Get a committed vendor resolution date.", "Confirm which activities can run in parallel and quantify remaining contingency.", "Set an early go/no-go checkpoint for the launch date."],
    "leadership_attention": {"decision_or_escalation": "Escalate vendor resolution and confirm whether the launch runway remains achievable.", "why_now": "Known work already consumes most of the four-week window."},
    "facts": ["Development is 80% complete.", "Four weeks remain before go-live.", "Security review requires two weeks and has not started.", "Vendor API resolution may take up to one week."],
    "inferences": ["The remaining schedule has limited contingency.", "Parallel execution may be required to protect the launch date."]
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
        messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": update[:12000]}],
    )
    result = json.loads(response.choices[0].message.content)
    validate_result(result)
    return result


def validate_result(result: dict[str, Any]) -> None:
    required = {"executive_summary", "program_health", "delivery_intelligence", "risks", "blockers", "dependencies", "recommended_next_actions", "leadership_attention", "facts", "inferences"}
    missing = required - result.keys()
    if missing:
        raise ValueError(f"Model response is missing fields: {', '.join(sorted(missing))}")
    if result["program_health"].get("status") not in {"Green", "Amber", "Red"}:
        raise ValueError("Program health status must be Green, Amber, or Red")


def _status_class(value: str) -> str:
    normalized = value.lower()
    if normalized in {"red", "high", "critical"}:
        return "red"
    if normalized in {"amber", "medium", "moderate"}:
        return "amber"
    if normalized == "green":
        return "green"
    return "neutral"


def _contingency_class(value: str) -> str:
    normalized = value.lower()
    if any(term in normalized for term in ["none", "zero", "low", "minimal", "limited", "insufficient", "inadequate"]):
        return "red"
    if any(term in normalized for term in ["medium", "moderate"]):
        return "amber"
    if any(term in normalized for term in ["high", "adequate", "healthy", "strong"]):
        return "green"
    return "neutral"


def _pressure_width(value: str) -> int:
    normalized = value.lower()
    if normalized in {"high", "critical"}:
        return 90
    if normalized in {"medium", "moderate", "amber"}:
        return 60
    if normalized in {"low", "green"}:
        return 30
    return 45


def render_snapshot(result: dict[str, Any]) -> None:
    health = result["program_health"]
    delivery = result["delivery_intelligence"]
    blockers = len(result.get("blockers", []))
    dependencies = len(result.get("dependencies", []))
    status = health.get("status", "Unknown")
    pressure = delivery.get("schedule_pressure", "Not established")
    contingency = delivery.get("contingency_assessment", "Not established")

    st.subheader("📊 Executive Snapshot")
    cards = [
        ("Program Health", status, _status_class(status)),
        ("Schedule Pressure", pressure, _status_class(pressure)),
        ("Contingency", contingency, _contingency_class(contingency)),
        ("Blockers", str(blockers), "red" if blockers else "green"),
    ]
    card_html = "<div class='snapshot-grid'>"
    for label, value, css_class in cards:
        card_html += f"<div class='snapshot-card'><div class='snapshot-label'>{label}</div><div class='snapshot-value {css_class}'>{value}</div></div>"
    card_html += "</div>"
    st.markdown(card_html, unsafe_allow_html=True)
    st.markdown(f"<div class='attention-strip'><strong>Dependencies:</strong> {dependencies} &nbsp; • &nbsp; <strong>Health rationale:</strong> {health.get('reason', 'Not established')}</div>", unsafe_allow_html=True)


def render_timeline_visual(result: dict[str, Any]) -> None:
    delivery = result["delivery_intelligence"]
    facts = result.get("facts", [])
    timeline_facts = [fact for fact in facts if any(token in fact.lower() for token in ["day", "week", "month", "deadline", "launch", "go-live"])]

    st.subheader("⏱️ Timeline Pressure")
    if timeline_facts:
        for fact in timeline_facts[:5]:
            st.markdown(f"<div class='timeline-item'>• {fact}</div>", unsafe_allow_html=True)
    else:
        st.info("The input does not contain enough timing information for a meaningful timeline view.")

    pressure = delivery.get("schedule_pressure", "Not established")
    contingency = delivery.get("contingency_assessment", "Not established")
    width = _pressure_width(pressure)
    pressure_class = _status_class(pressure)
    st.markdown(f"<div class='pressure-bar'><div class='pressure-fill {pressure_class}' style='width:{width}%'></div></div><div class='pressure-caption'><strong>Schedule pressure:</strong> {pressure} &nbsp; • &nbsp; <strong>Contingency:</strong> {contingency}</div>", unsafe_allow_html=True)


def render_result(result: dict[str, Any]) -> None:
    health = result["program_health"]
    delivery = result["delivery_intelligence"]
    leadership = result["leadership_attention"]

    st.markdown("""<style>
    .snapshot-grid {display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:8px 0 14px;}
    .snapshot-card {padding:16px;border:1px solid rgba(128,128,128,.28);border-radius:10px;background:rgba(128,128,128,.07);min-height:82px;}
    .snapshot-label {font-size:13px;opacity:.72;margin-bottom:8px;}
    .snapshot-value {font-size:20px;font-weight:700;line-height:1.25;}
    .snapshot-value.red {color:#ff6b6b;}.snapshot-value.amber {color:#f0ad4e;}.snapshot-value.green {color:#5cb85c;}.snapshot-value.neutral {color:inherit;}
    .attention-strip {padding:12px 14px;border-left:4px solid rgba(128,128,128,.55);background:rgba(128,128,128,.07);border-radius:6px;margin-bottom:16px;}
    .timeline-item {padding:7px 10px;margin:5px 0;border-left:3px solid rgba(128,128,128,.45);background:rgba(128,128,128,.05);border-radius:4px;}
    .pressure-bar {height:10px;background:rgba(128,128,128,.18);border-radius:8px;overflow:hidden;margin-top:12px;}
    .pressure-fill {height:100%;border-radius:8px;}.pressure-fill.red {background:#d9534f;}.pressure-fill.amber {background:#f0ad4e;}.pressure-fill.green {background:#5cb85c;}.pressure-fill.neutral {background:#888;}
    .pressure-caption {font-size:13px;opacity:.8;margin:7px 0 16px;}
    @media (max-width: 800px) {.snapshot-grid {grid-template-columns:repeat(2,1fr);}}
    </style>""", unsafe_allow_html=True)

    render_snapshot(result)

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

    render_timeline_visual(result)

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
    st.write("This portfolio application converts an unstructured program update into program health, delivery intelligence, risks, blockers, dependencies, actions, and leadership attention. The TPM remains accountable for validation and decisions.")

sample = """Development is 80% complete with 4 weeks remaining before go-live.
The security review has not started and requires 2 weeks.
A vendor API issue is unresolved and may take up to 1 week to fix.
The team still needs to complete final development and integration testing."""

update = st.text_area("Paste a program update", value=sample, height=180, max_chars=12000, help="Use synthetic or non-confidential information for this portfolio demo.")

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
