<!-- prompts/after_step_review.md -->

You have just **completed or attempted a step** in PLAN.md.

**Do the following:**

1. **Update PLAN.md**

   - Mark the step’s Status (Complete / In Progress / Blocked).
   - If new info changes Dependencies, add/update them.
   - If new paradigms, patterns, or file references emerged, add a short note in the step or in “Next Review & Re-Prioritization Notes”.

2. **Unknowns**

   - Add any newly discovered unknowns under “Open Questions / Unknowns”.
   - For each unknown: short description, owner (if known), and proposed next step (spike or decision).

3. **Reprioritize**

   - Reorder remaining steps so the **shortest path to the next demo** is on top.
   - If scope changed, reflect it explicitly.

4. **State & Log**
   - Update `memory/activeContext.md` with:
     - Current Milestone
     - Next Actionable Step (exact step text)
   - Append a dated note in `records/progress.log.md`:
     - What was done (or attempted)
     - Outcome (pass/fail/partial)
     - Any new dependencies/unknowns
     - Link to artifacts (code paths, docs, commits)

**Guardrails**

- Do not introduce CI/CD or deployment tasks unless a working demo exists and the next bottleneck is release-ability.
- If blocked, propose the **smallest spike** that unblocks and insert it at the top of the plan.
