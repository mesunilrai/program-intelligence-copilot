# Program Intelligence Copilot

> **AI-assisted program intelligence for Technical Program Managers**
>
> Turns an unstructured program update into an executive-ready view of **program health, delivery pressure, risks, blockers, dependencies, actions, and leadership attention**.

**Portfolio V1 • Python • Streamlit • Groq LLM • Structured JSON • Human-in-the-loop**

## Table of Contents

- [Why this project](#why-this-project)
- [What it demonstrates](#what-it-demonstrates)
- [The TPM problem](#the-tpm-problem)
- [How it works](#how-it-works)
- [Key capabilities](#key-capabilities)
- [Example](#example)
- [AI approach and guardrails](#ai-approach-and-guardrails)
- [Architecture](#architecture)
- [Technology](#technology)
- [Responsible AI](#responsible-ai)
- [Limitations](#limitations)
- [Run locally](#run-locally)
- [Project status](#project-status)
- [Portfolio context](#portfolio-context)

## Why this project

Technical Program Managers routinely receive fragmented updates from engineering, product, vendors, security, operations, and other stakeholders. The difficult part is not producing another summary—it is identifying **what changed, what matters, what is at risk, what depends on something else, and what needs a decision**.

Program Intelligence Copilot explores how AI can shorten the path from a raw program update to useful delivery intelligence while keeping the TPM accountable for validation and decisions.

## What it demonstrates

This portfolio project demonstrates practical application of AI to TPM work:

- Converts unstructured program updates into structured delivery intelligence
- Assesses overall **program health** with an evidence-based rationale
- Surfaces **risks, blockers, and dependencies**
- Evaluates **schedule pressure and delivery contingency** when timing information supports it
- Produces prioritized **recommended next actions**
- Identifies issues requiring **leadership attention or escalation**
- Separates **explicit facts from AI inferences** so the output can be reviewed
- Uses guardrails to reduce unsupported risks, blockers, and dependencies
- Presents the result as an executive-friendly dashboard rather than a generic chatbot response

## The TPM problem

A typical status update might say:

> Development is 80% complete. Four weeks remain. Security review has not started and requires two weeks. A vendor API issue may take up to one week to resolve.

A useful TPM response should not simply repeat those facts. It should identify the delivery implication:

**The schedule is under pressure because known work consumes most of the remaining runway, leaving limited contingency for additional defects or delays.**

That distinction—**information → implication → action**—is the core product idea.

## How it works

```text
Unstructured Program Update
            ↓
      LLM-assisted Analysis
            ↓
   Structured JSON Validation
            ↓
 ┌──────────┼───────────┐
 ↓          ↓           ↓
Health     Risks    Dependencies
 ↓          ↓           ↓
Delivery   Blockers   Actions
Intelligence            ↓
                 Leadership Attention
            ↓
      Executive Snapshot
```

The application also keeps **facts** and **AI inferences** separate, allowing the TPM to see what came directly from the update versus what the model concluded from those facts.

## Key capabilities

### 📊 Executive Snapshot

Provides an at-a-glance view of:

- Program health
- Schedule pressure
- Contingency
- Blocker count
- Dependency count and health rationale

### 🧠 Delivery Intelligence

Analyzes the delivery situation using available timing signals, including remaining runway, known activity duration, sequencing, schedule pressure, and contingency.

### ⚠️ Risk and dependency intelligence

For identified risks, the application presents:

- Risk
- Impact
- Mitigation

Dependencies include why the dependency matters to delivery.

### 🎯 Recommended actions

Turns identified issues into concise, prioritized next actions instead of stopping at a summary.

### 🚨 Leadership attention

Highlights the decision or escalation that may require leadership attention and explains why it matters now.

### 🔎 Explainability

The output explicitly separates:

- **Facts** — information extracted from the supplied update
- **AI Inferences** — conclusions derived from those facts

This is intentional. The goal is decision support, not opaque automation.

## Example

### Input

```text
Development is 80% complete with 4 weeks remaining before go-live.
Security review has not started and requires 2 weeks.
A vendor API issue is unresolved and may take up to 1 week to fix.
The team still needs to complete final development and integration testing.
```

### Intended output

**Program Health: Amber**

**Delivery implication:** The remaining work consumes a significant portion of the four-week runway, creating high schedule pressure and limited contingency.

**Recommended attention:**

1. Start the security review immediately.
2. Obtain a committed vendor resolution date.
3. Confirm which activities can run in parallel.
4. Establish an early go/no-go checkpoint.

The example illustrates the intended reasoning pattern. It is not presented as evidence that the application can make autonomous delivery decisions.

## AI approach and guardrails

The project is intentionally focused on **decision support rather than autonomous program management**.

| Principle | Application |
|---|---|
| Evidence first | Base conclusions on information supplied in the program update. |
| Preserve explicit facts | Do not contradict information explicitly provided by the user. |
| Avoid unsupported inference | Do not create a risk, blocker, or dependency simply because information is unknown. |
| Explicit uncertainty | Surface uncertainty when the available evidence is insufficient. |
| Structured output | Use predictable fields for consistent rendering and validation. |
| Action orientation | Convert meaningful observations into practical next actions. |
| Human accountability | The TPM reviews and owns the final interpretation and decision. |

The application validates the expected JSON structure before rendering an AI response. If the AI provider is unavailable, the portfolio demo can fall back to a clearly identified built-in sample analysis rather than presenting that sample as AI-generated analysis of the user's input.

## Architecture

The implemented V1 architecture is deliberately lightweight:

```text
┌─────────────────────────┐
│ Streamlit User Interface│
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│ TPM Program Update      │
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│ Groq LLM Analysis       │
│ + TPM System Prompt     │
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│ Structured JSON Output  │
│ + Schema Validation     │
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│ Executive Dashboard     │
│ + Decision Support      │
└─────────────────────────┘
```

The application is intentionally small enough to understand and run locally while demonstrating the product and reasoning layer of an AI-enabled TPM solution.

## Technology

- **Python** — application logic
- **Streamlit** — interactive web UI
- **Groq API / LLM** — AI-assisted program analysis
- **Structured JSON** — predictable model output
- **Prompt guardrails** — evidence, uncertainty, and decision-support controls

The differentiator is not the framework choice; it is how the AI capability is applied to a concrete TPM workflow.

## Responsible AI

This is a portfolio application using synthetic or non-confidential information.

Important usage boundaries:

- Do not submit proprietary or confidential company information to an external model without appropriate authorization.
- Do not expose API keys, credentials, personal data, or sensitive architecture information in prompts or logs.
- Treat model output as decision support, not an authoritative source of truth.
- Validate AI output before using it for consequential program decisions.
- Production deployment would require appropriate authentication, privacy controls, rate limiting, observability, cost controls, and reliability mechanisms.

## Limitations

This V1 intentionally does **not** claim autonomous program management or guaranteed factual correctness.

Current limitations include:

- Model output can be incomplete or incorrect.
- Schedule reasoning depends on the quality and completeness of the supplied information.
- The system cannot identify hidden dependencies that were not provided.
- Risk severity and program health still require human context.
- The current application does not maintain historical program state.
- It is not integrated with enterprise systems such as Jira, Azure DevOps, Smartsheet, or similar delivery platforms.
- Production use would require stronger security, privacy, reliability, and operational controls.

## Run locally

### 1. Clone the repository

```bash
git clone https://github.com/mesunilrai/program-intelligence-copilot.git
cd program-intelligence-copilot
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Groq API key

Set `GROQ_API_KEY` as an environment variable. Do not commit the key to GitHub.

Windows Command Prompt:

```cmd
set GROQ_API_KEY=your_key_here
```

### 5. Run the application

```bash
streamlit run app.py
```

If no API key is configured, the application can demonstrate the portfolio workflow using its clearly labelled built-in sample analysis.

## Project status

### V1 — Portfolio MVP ✅

- [x] TPM problem and target workflow defined
- [x] AI-assisted structured analysis
- [x] Program health assessment
- [x] Delivery intelligence and schedule pressure
- [x] Risk, blocker, and dependency analysis
- [x] Recommended next actions
- [x] Leadership attention
- [x] Facts vs. AI inference separation
- [x] AI inference guardrails
- [x] Executive dashboard visualization
- [x] Local testing across Green, Amber, and Red scenarios
- [x] Zero-state handling for empty risks, blockers, and dependencies

The MVP is intentionally frozen at this point. Future enhancements will be considered separately rather than expanding the portfolio MVP unnecessarily.

## Portfolio context

This project complements my **AI TPM Claude Skills** repository rather than duplicating it.

- **AI TPM Claude Skills** demonstrates reusable AI workflow and reasoning design for TPM activities.
- **Program Intelligence Copilot** demonstrates the product/application layer: turning an AI-assisted TPM workflow into a usable software experience.

Together they demonstrate a broader approach to **AI + Technical Program Management** across workflow design, reasoning, product thinking, and application implementation.

---

### About

Built as a practical portfolio project by **Sunil Rai**, Technical Program Manager focused on AI-enabled program intelligence, engineering delivery, digital transformation, and technical decision support.

*Portfolio project. Uses synthetic examples and does not contain proprietary company information.*
