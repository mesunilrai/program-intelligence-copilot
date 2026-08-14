# Program Intelligence Copilot

> An AI-assisted technical program management application that turns unstructured program updates into structured delivery intelligence.

[![Status](https://img.shields.io/badge/status-portfolio%20V1-blue)](https://github.com/mesunilrai/program-intelligence-copilot)

## Table of Contents

- [Why this project](#why-this-project)
- [What it does](#what-it-does)
- [The TPM problem](#the-tpm-problem)
- [How it works](#how-it-works)
- [Example](#example)
- [AI approach](#ai-approach)
- [Architecture](#architecture)
- [Why it matters](#why-it-matters)
- [Security and responsible AI](#security-and-responsible-ai)
- [Limitations](#limitations)
- [Roadmap](#roadmap)
- [Portfolio context](#portfolio-context)

## Why this project

Technical program managers routinely receive fragmented updates from engineering, product, vendors, security, operations, and other stakeholders. The difficult part is not producing another summary—it is identifying **what changed, what matters, what is at risk, and what needs a decision**.

Program Intelligence Copilot explores how an AI application can help a TPM move from raw updates to structured program intelligence while keeping the TPM responsible for validation and decisions.

## What it does

The portfolio V1 is designed around a simple workflow:

```text
Unstructured Program Update
            ↓
      AI-assisted Analysis
            ↓
 ┌──────────┼───────────┐
 ↓          ↓           ↓
Health     Risks    Dependencies
 ↓          ↓           ↓
Blockers   Impact    Actions
            ↓
     Leadership Attention
```

The target output is a concise program view covering:

- **Executive summary** — what changed and why it matters
- **Program health** — overall delivery signal with rationale
- **Risks** — potential future events, impact, and mitigation
- **Blockers** — issues currently preventing progress
- **Dependencies** — teams, systems, vendors, or decisions required
- **Recommended next actions** — concrete actions and priorities

## The TPM problem

A typical status update might say:

> Development is 80% complete. Four weeks remain. Security review has not started and requires two weeks. A vendor API issue may take up to one week to resolve.

A useful TPM response should not simply repeat those facts. It should identify the delivery implication:

**The schedule is Amber because the remaining security review, vendor resolution, development, integration, and testing consume most of the remaining runway with little contingency.**

That distinction—**information → implication → action**—is the core product idea.

## How it works

1. **Capture** — TPM provides an unstructured program update.
2. **Interpret** — the AI identifies delivery signals, entities, constraints, and relationships.
3. **Structure** — signals are organized into health, risks, blockers, dependencies, and actions.
4. **Reason** — the application evaluates schedule pressure, dependencies, and potential impact where the available information supports it.
5. **Communicate** — results are presented in an executive-friendly format.
6. **Review** — the TPM validates assumptions, fills information gaps, and owns the final decision.

The application should distinguish **facts provided by the user** from **AI interpretation or inference**. Where an important relationship is unknown, the system should surface it as an uncertainty rather than silently inventing one.

## Example

### Input

```text
Development is 80% complete with 4 weeks remaining before go-live.
Security review has not started and normally requires 2 weeks.
A vendor API issue is unresolved and may take up to 1 week to fix.
```

### Example output

**Program Health: Amber — At Risk**

**Why:** The mandatory security review consumes half of the remaining runway. The vendor issue and remaining development/testing create a compressed schedule with limited contingency.

**Critical attention:**

1. Start the security review immediately.
2. Obtain a firm vendor resolution date.
3. Confirm whether the API issue blocks or can run in parallel with security testing.
4. Establish an early go/no-go checkpoint.

The example demonstrates the intended reasoning pattern; it is not presented as evidence that the application can make autonomous delivery decisions.

## AI approach

The project is intentionally focused on **decision support rather than autonomous program management**.

Key design principles:

| Principle | Application |
|---|---|
| Evidence first | Base conclusions on information supplied in the program update. |
| Explicit uncertainty | Surface missing or ambiguous dependencies instead of guessing. |
| Structured output | Use predictable sections so results can be consumed consistently. |
| Action orientation | Convert observations into practical next actions. |
| Human accountability | TPM reviews and owns the final interpretation and decision. |
| Evaluation | Test outputs against representative scenarios, not just whether the response sounds good. |

## Architecture

The intended V1 architecture is deliberately simple:

```text
┌──────────────────────┐
│ TPM / Program Update │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Application / UI     │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Analysis API         │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ LLM / AI Reasoning   │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Structured Program   │
│ Intelligence Output  │
└──────────────────────┘
```

Implementation details will evolve as the application is hardened. The architecture documentation records the design assumptions separately from capabilities that have been implemented and tested.

## Why it matters

For a TPM, the potential value is not simply saving time writing status reports. The larger opportunity is to improve the **signal-to-decision path**:

```text
Many Updates
     ↓
Relevant Signals
     ↓
Delivery Implications
     ↓
Prioritized Actions
     ↓
Better Human Decisions
```

This is the area where I am interested in applying AI to real TPM work: reducing cognitive overhead while preserving judgment, context, and accountability.

## Security and responsible AI

The project is intended as a portfolio application using synthetic or non-confidential information.

Key considerations include:

- Do not submit proprietary or confidential company information to an external model without appropriate authorization.
- Avoid exposing credentials, tokens, personal data, or sensitive architecture details in prompts or logs.
- Apply authentication and rate limiting before exposing an AI endpoint publicly.
- Treat model output as decision support, not an authoritative source of truth.
- Make uncertainty and missing information visible to the user.
- Validate model output before using it in consequential program decisions.

See [`docs/security.md`](docs/security.md) for the current security checklist.

## Limitations

This portfolio V1 intentionally does **not** claim autonomous program management or guaranteed factual correctness.

Current limitations include:

- Model output can be incomplete or incorrect.
- Schedule reasoning depends on the quality and completeness of the supplied information.
- The system cannot know hidden dependencies that were not provided.
- Risk severity and program health require human context.
- Production use would require stronger controls for authentication, privacy, observability, cost, and reliability.

## Roadmap

### V1 — Portfolio foundation

- [x] Define the TPM problem and target workflow
- [x] Establish structured program-intelligence output
- [x] Document AI principles and responsible-use boundaries
- [ ] Finalize application implementation and tested demo

### V1.1 — Evaluation

- Representative synthetic program scenarios
- Expected-output criteria
- Regression evaluation
- Failure-mode analysis

### Future

- Historical trend analysis
- Dependency graph visualization
- Change-impact analysis
- Decision tracking
- Program-level portfolio rollups

Features will be added only where they provide meaningful TPM value; the project is intentionally not designed to become a generic AI chatbot.

## Portfolio context

This project complements my **AI TPM Claude Skills** repository rather than duplicating it.

- **AI TPM Claude Skills** demonstrates reusable AI workflow and reasoning design for TPM activities.
- **Program Intelligence Copilot** demonstrates the product/application layer: turning an AI-assisted TPM workflow into a usable software experience.

Together they show a broader approach to AI + Technical Program Management across **workflow design, reasoning, product thinking, and application implementation**.

---

### About

Built as a practical portfolio project by **Sunil Rai**, Technical Program Manager focused on AI-enabled program intelligence, engineering delivery, digital transformation, and technical decision support.

*Portfolio project. Uses synthetic examples and does not contain proprietary company information.*
