# Security & Responsible AI

## Portfolio boundary

This project is a portfolio application. Use synthetic or non-confidential information for demonstrations.

## Secrets

- API keys must be supplied through environment variables or a managed secret store.
- Never commit `.env`, provider keys, tokens, or credentials.
- The application intentionally avoids displaying raw provider errors to users.

## Data handling

Before production use, define data classification rules and prevent sensitive program information from being sent to an external model without authorization.

## AI output

Model output is advisory. A TPM must validate facts, assumptions, dependencies, risk severity, and recommended actions before using the output for consequential decisions.

## Production hardening

A production deployment would require authentication/authorization, rate limiting, structured audit logging, privacy controls, input/output filtering, provider monitoring, cost controls, model/version tracking, and systematic evaluation.
