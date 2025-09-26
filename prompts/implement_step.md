<!-- prompts/implement_step.md -->

You are in **Act Mode** implementing the **Next Actionable Step**.

**Inputs**

- PLAN.md
- memory/activeContext.md (read Next Actionable Step ID/title)
- prompts/execution_guardrails.md (follow strictly)
- records/progress.log.md (append outcome)
- records/friction.log.md (append if friction occurs)
- repo files (discover build/test/run cmds)

**Procedure**

0. **Identify the Step**

   - Read memory/activeContext.md → `Next Actionable Step (ID + title)`.
   - Locate the step in PLAN.md and restate its **Acceptance Criteria** and **Testing Instructions** verbatim.

1. **Preparation**

   - Detect project commands (e.g., `package.json` scripts, Makefile, poetry/pip, etc.).
   - Propose a **Command Plan**: ordered list of terminal commands required (install/build/run/tests), clearly marked as _to be executed_.
   - Propose **File Edit Plan**: list of files to touch with a 1–2 line intent per file.
   - **WAIT for explicit APPROVAL** before running commands. If user replies “APPROVE”, continue; otherwise refine.

2. **Execute (with Guardrails)**

   - Create a working branch: `git checkout -b feat/<STEP-ID>-<slug>`.
   - Apply minimal, reviewable edits; show a brief diff summary as you go.
   - Execute commands from the approved Command Plan.
   - If a command fails, attempt up to **2** refined retries.
   - On repeat failures, immediately capture a **Friction Incident** (see step 5).

3. **Validate**

   - Run the step’s **Testing Instructions** exactly as written (or update them if they were incomplete).
   - Map each **Acceptance Criterion** → **Pass/Fail** with evidence (CLI output paths, screenshots dir, or artifact links).

4. **Commit & Record**

   - Commit with Conventional Commit style:
     - `feat(<area>): implement <STEP-ID> - <short description>`
     - Body includes: rationale, files changed, links to PLAN.md step.
   - Append a dated entry to `records/progress.log.md`:
     - Step ID/title, outcome (pass/partial/fail), key diffs, artifacts/links.

5. **Friction Handling (if any)**

   - If 3 retries of a command or >45m blocked or repeated edits without passing tests:
     - Append to `records/friction.log.md` with symptom, suspected cause, workaround, and links.
     - Add/Update an Unknown in PLAN.md if the acceptance criteria were ambiguous or dependencies were missing.

6. **Close the Loop**
   - Run the **after-step review** ritual (prompts/after_step_review.md) to:
     - Update step Status, Dependencies, Unknowns.
     - Reorder remaining steps toward the next demo.
     - Refresh memory/activeContext.md (must point to a single next step).

**Output**

- Code edits applied, tests executed, commit created.
- `records/progress.log.md` entry appended.
- `records/friction.log.md` entry appended if applicable.
- PLAN.md updated via after-step review.

**Constraints**

- Follow prompts/execution_guardrails.md strictly.
- Never alter `.clinerules` directly; queue proposals in records/rule_proposals.md.
