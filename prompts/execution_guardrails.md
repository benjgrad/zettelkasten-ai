<!-- prompts/execution_guardrails.md -->

**Execution Guardrails**

- **Confirmation Gate:** Do not run any terminal command until the user types **APPROVE** to your Command Plan.
- **Non-Destructive Default:** Avoid destructive commands (`rm -rf`, force pushes, dropping DBs). If absolutely required, request explicit approval and show a safe alternative or a dry-run.
- **Minimal Diffs:** Keep changes small and reviewable; avoid sweeping refactors unless the step’s ACs demand it.
- **Local First:** Prefer local runs & tests. No CI/CD, infra, or deployment until a working demo exists and the plan explicitly prioritizes it.
- **Secrets & Env:** Never hardcode secrets or modify global environment without user consent.
- **Logging:** Capture meaningful excerpts (last 50–200 lines) of any failing command to `records/progress.log.md` and `records/friction.log.md` as needed.
- **Retry Budget:** Max 2 refined retries per failing command. After that, log friction and propose a smallest-possible spike.
- **Exit Criteria:** A step is “Done” only when all Acceptance Criteria are evidenced as “Pass”. Otherwise mark Partial/Blocked and run after-step review.
