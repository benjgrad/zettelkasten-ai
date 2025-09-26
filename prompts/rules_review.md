<!-- prompts/rules_review.md -->

You are conducting a **Rules Review** of our AI-driven development process.

**Inputs**

- PLAN.md
- records/progress.log.md
- records/friction.log.md
- .clinerules (read-only; do not modify directly)
- records/rule_proposals.md (append here)

**Do**

1. Summarize friction since the last review (group by root cause).
2. For each cluster, write a **Rule Change Proposal**:
   - Problem (with examples/links)
   - Proposed change (exact snippet to add/edit in .clinerules)
   - Expected impact (benefits/risks)
   - Validation plan (how we’ll know it helped)
   - Version bump (minor) suggestion
3. Append proposals to `records/rule_proposals.md` with today’s date.
4. In `PLAN.md → Next Review & Re-Prioritization Notes`, add any process changes that affect the near-term plan.

**Guardrails**

- Do not edit `.clinerules` directly; only propose diffs.
- Keep proposals small and testable.
