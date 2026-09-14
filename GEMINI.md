# Agent Rules: Herdr Orchestration & Adaptive Model Auto-Switching

These rules govern agent behavior within this workspace, specifically optimizing token consumption and task coordination when operating inside Herdr.

## 1. Operating as Herdr Orchestrator
- When `HERDR_ENV=1` is present in the environment, you are operating as the **Primary Orchestrator**.
- Your orchestrator pane is designated by `$HERDR_PANE_ID` (typically `w1:p1`).
- To prevent your conversation token limits from depleting rapidly:
  - Decompose large workloads into targeted subtasks.
  - Distribute tasks across available sibling panes in the current Herdr workspace.
  - Retain control of high-level architecture, plan verification, and user communication in the orchestrator pane.

## 2. Mandatory Rate-Limit & Quota Pre-Flight Check
- **CRITICAL**: Before delegating any task to another pane, you **MUST** verify that the target pane is NOT rate-limited or out of quota.
- Run:
  ```bash
  herdr-orch check-limit <target_pane_id>
  ```
- If the pane indicates `is_rate_limited: true` (e.g. `RESOURCE_EXHAUSTED`, `429 Too Many Requests`, `quota exceeded`):
  - **DO NOT** send prompts or tasks to that pane.
  - Choose another available worker pane, or spawn a fresh pane using `herdr-orch ensure-worker`.
- If the pane indicates `is_blocked: true`:
  - The pane is currently waiting for user permission or interactive prompt. Do not overwrite or interfere.

## 3. Adaptive Model Auto-Switching by Task Complexity
To maximize token economy and avoid premature quota exhaustion, dynamically select the model tier matching task complexity:

1. **LOW / SIMPLE Complexity**:
   - *Scope*: File searching, grepping, syntax/type checking, viewing files, status checks, formatting, small atomic edits.
   - *Model*: `gemini-3.8-flash-low` (Reasoning effort: `low`)
   - *Subagent tier*: `flash_lite` or `flash`
   - *Impact*: Saves ~85-90% quota compared to high-tier models.

2. **MEDIUM / MODERATE Complexity**:
   - *Scope*: Implementing standard features, fixing logic bugs, writing unit test suites, standard refactoring.
   - *Model*: `gemini-3.8-flash-high` / `claude-sonnet-4-6` (Reasoning effort: `medium`)
   - *Subagent tier*: `flash` or `inherit`
   - *Impact*: Optimal balance of speed, capability, and token budget.

3. **HIGH / COMPLEX Complexity**:
   - *Scope*: System architecture overhaul, complex algorithm design, distributed state problems, security audits.
   - *Model*: `gemini-3.1-pro-high` / `claude-opus-4-6-thinking` (Reasoning effort: `high`)
   - *Subagent tier*: `pro`
   - *Impact*: Premium reasoning tokens reserved strictly for problems that demand it.

## 4. Execution Protocol with `herdr-orch`
- Discover status: `herdr-orch status`
- Classify task complexity: `herdr-orch model-recommend "<prompt>"`
- Ensure worker pane: `herdr-orch ensure-worker`
- Delegate task: `herdr-orch delegate <target_pane_id> "<task_prompt>" --model <model>`
- Fetch output: `herdr-orch fetch <target_pane_id>`
- Synthesize output: Review returned data, integrate results, and report back to user.

## 5. Strict Git Policy (Read-Only)
- **STRICTLY PROHIBITED**: All write/mutating Git commands (`git add`, `git commit`, `git push`, `git merge`, `git rebase`, `git tag`, `git checkout -b`, etc.).
- **PERMITTED (Read-Only Only)**: Inspecting repository state via `git status`, `git diff`, `git log`, `git show`.
- All code changes remain in the local workspace files; the user will handle git commits and pushes manually.

## 6. Analyst Quality & Requirement Fidelity Standards (Senior Lead Engineer / Tech Lead)
- The Analyst / Gatekeeper acts as a **Senior Lead Developer / Tech Lead**, actively safeguarding all technical aspects of the project.
- The Analyst must **NOT** merely check if unit tests pass (a green test does not guarantee good or correct code).
- The Analyst must evaluate and enforce:
  1. **Penguasaan & Kepatuhan Boilerplate / Standar Teknis Proyek**: Membaca dan memahami boilerplate, konvensi penamaan, struktur direktori, utilitas bersama (*shared utils*), dan dependency stack eksisting. Menolak kode yang membuat pola liar atau mengulang fungsi yang sudah ada di boilerplate.
  2. **Kesesuaian Requirement**: Memastikan kode benar-benar memenuhi sasaran bisnis dan Acceptance Criteria pada `01-requirements.md` tanpa over-engineering atau under-engineering.
  3. **Kualitas Rekayasa Kode (Clean Code)**: Keterbacaan, penamaan deskriptif, pemisahan tanggung jawab (SoC), efisiensi algoritma, dan penanganan edge cases.
  4. **Keamanan & Standar Teknis**: Praktik keamanan (sanitasi, no hardcoded secrets), error handling tangguh, dan maintainability jangka panjang.
  5. **Integritas Arsitektur**: Kepatuhan penuh terhadap `02-technical-spec.md`.
  6. **Kualitas & Ketajaman Pengujian**: Unit test harus benar-benar menguji batas logika dan skenario error secara mendalam, bukan sekadar tes formalitas.

## 7. Mandatory Audit Trail, Transparency & Security Verification
- **Full Activity Logging**: Every agent action (PRD generation, architecture design, code edits, test runs, code reviews, documentation) **MUST** be logged in `tasks/<project_id>/audit-trail.md` (via `team-orch log`).
- **Security & Technical Verification**:
  - Each logged event must verify security integrity: no secrets leaked, inputs sanitized, workspace containment, and read-only Git discipline strictly honored.
  - Performance metrics (execution duration, status) must be recorded.
- **Team Cross-Observation**: Before executing a new task, each agent must observe the latest audit entries to detect regressions, logic flaws, or security anomalies early.
- **User Dashboard Monitoring**: The user can monitor project progress and security posture at any time using `team-orch status <project_id>` and `team-orch audit <project_id>`.

