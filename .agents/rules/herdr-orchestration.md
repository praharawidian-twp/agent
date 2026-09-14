# Herdr Cross-Pane Orchestration & Adaptive Model Selection Rules

When running within Herdr (`HERDR_ENV=1`):

1. **Topology Discovery**:
   - The current pane is the Orchestrator.
   - Sibling panes in the same workspace are Worker Panes.
   - Use `herdr-orch status` to list active panes.

2. **Pre-flight Rate Limit Safeguard**:
   - Always run `herdr-orch check-limit <pane_id>` before assigning any task.
   - If `is_rate_limited` is true, avoid delegating to that pane.

3. **Task Complexity Auto-Switching**:
   - Low complexity -> `gemini-3.8-flash-low` / `flash_lite`
   - Medium complexity -> `gemini-3.8-flash-high` / `flash`
   - High complexity -> `gemini-3.1-pro-high` / `pro`

4. **Delegation & Fetching**:
   - Use `herdr-orch delegate <pane_id> "<task>" [--model <model>]` to dispatch.
   - Use `herdr-orch fetch <pane_id>` to read response.
   - Process and synthesize results in the orchestrator conversation.
