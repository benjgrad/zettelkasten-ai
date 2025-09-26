<!-- prompts/friction_capture.md -->

You are capturing a **Friction Incident**.

**Inputs**

- The last attempted step (from PLAN.md and memory/activeContext.md)
- Console output or edit history if available

**Do**

- Append to `records/friction.log.md`:

  - Date/Time
  - Step ID/Title
  - Symptom (what slowed us)
  - Suspected cause (rule gap/conflict/missing template/other)
  - Immediate workaround taken
  - Links (commits, PRs, files, logs)

- If two or more similar incidents exist, add a short note in `records/rule_proposals.md` referencing this pattern (to be formalized during the next rules_review).
