# Rule Change Proposals

## 2025-09-30 — Proposal RP-0001

- Problem: Repeated terminal retries for setup commands are not caught early.
- Proposed .clinerules edit:
  [signals]
  - "If a setup command fails twice, require a 'Setup Spike' step with concrete reproduction steps and a cached log excerpt."
- Expected Impact: Faster detection; fewer thrash cycles.
- Validation Plan: Next 2 milestones should show <50% setup failures in progress.log.
- Suggested Version: 1.2
- Status: Pending review
