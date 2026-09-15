# Herdr Cross-Pane Orchestration & Autonomous Fleet Rules

When running within Herdr (`HERDR_ENV=1`):

## 1. Dedicated Pane Architecture (1 Role = 1 Dedicated Pane)
- **Control Room (Orchestrator / PM)**:
  - Designated by `$HERDR_PANE_ID` (typically `w1:p4`).
  - **Exclusively reserved** for human-agent interaction, high-level orchestration, and mission monitoring.
  - **STRICTLY PROHIBITED**: Running long-running commands, heavy coding, or multi-step execution loops directly in the Control Room pane. The Control Room must always remain responsive to user instructions.
- **Worker Panes**:
  - Each role operates in its own dedicated sibling pane:
    - **Analis / Senior Lead Engineer (Tech Lead)**: Dedicated pane (e.g. `w1:pA`).
    - **Coder / Developer**: Dedicated pane (e.g. `w1:p9`).
    - **Dokumenter / QA**: Spawned in a new split pane on demand (`herdr pane split`).

## 2. Mandatory `agy-auto` Session & Readiness Check
- Every worker pane must automatically operate within an `agy-auto` session matching its complexity tier:
  - Analis: `gemini-3.1-pro-high`
  - Coder: `gemini-3.8-flash-high`
  - Dokumenter: `gemini-3.8-flash-low`
- **Readiness Check for `agy-auto`**:
  - The system checks if `agy-auto` is installed and available in PATH.
  - If `agy-auto` is not found, the PM **must ask the user for permission** to create the wrapper script (`exec agy --dangerously-skip-permissions "$@"` at `~/.local/bin/agy-auto`). If approved, execute immediately.

## 3. Explicit Role Introduction (Self-Introduction)
- Every agent entering or executing in a pane **MUST** introduce its active role and scope at the very beginning of the turn:
  - Example: `"Halo Pengguna & Tim! Saya [Role]... Saya siap [Deskripsi tugas]..."`

## 4. Transparent Cross-Agent Communication
- Agents communicate and hand off work across panes in real time (e.g., Coder sends a Review Request to the Analis pane; Analis responds with Code Review and approval).
- The user can see all messages and execution outputs live in the corresponding Herdr terminal panes.

## 5. Status Alignment Protocol
- Before terminating, disabling, or changing the state of an `agy-auto` session in any pane, the PM **MUST** inform the user first to ensure mutual alignment.

## 6. Pre-flight Rate Limit Safeguard
- Always run `herdr-orch check-limit <pane_id>` before assigning any task.
- If `is_rate_limited` is true, avoid delegating to that pane.

## 7. Strict Git Read-Only Policy
- All agents are strictly prohibited from mutating Git state (`git add`, `git commit`, `git push`, etc.). Only inspection (`git status`, `git diff`, `git log`) is permitted.
