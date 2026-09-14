# Multi-Agent Coordination & Herdr Rules

- Workspace: Herdr multi-pane orchestration enabled.
- Primary role: Main session acts as Orchestrator.
- Subtask delegation: Always check target pane rate limits with `herdr-orch check-limit <pane_id>` prior to task delegation.
- Model auto-switch:
  - Low complexity -> `gemini-3.8-flash-low`
  - Medium complexity -> `gemini-3.8-flash-high`
  - High complexity -> `gemini-3.1-pro-high`
- Utility: `herdr-orch` CLI installed at `/Users/macbook/.local/bin/herdr-orch`.
- Git Policy (CRITICAL):
  - Agents are strictly FORBIDDEN from modifying Git state (`git add`, `git commit`, `git push`, `git merge`, etc.).
  - Only read-only inspections (`git status`, `git diff`, `git log`) are permitted.
- Analyst Evaluation Standard (Senior Lead Engineer / Tech Lead):
  - The Analyst acts as a **Senior Lead Developer / Tech Lead**, not just a passive reviewer.
  - The Analyst **MUST** read, understand, and enforce the project's existing boilerplate, architecture conventions, idioms, and technical standards.
  - The Analyst must **NOT** solely focus on passing unit tests.
  - The Analyst **MUST** thoroughly safeguard all technical aspects: clean code, security best practices, maintainability, edge cases, reusable utilities, and strict alignment with user requirements (`01-requirements.md`).
- Mandatory Audit Trail & Full Transparency:
  - Every agent (PM, Analis, Coder, Dokumenter) **MUST** record technical actions, commands, duration, and security checks into `tasks/<project_id>/audit-trail.md` (via `team-orch log`).
  - Every agent **MUST** observe preceding audit entries before acting to detect anomalies, regressions, or security concerns.
  - Real-time monitoring & overview available via `team-orch status <project_id>` and `team-orch audit <project_id>`.



