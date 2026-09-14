#!/usr/bin/env python3
"""
herdr-autoswitch.py - PreInvocation hook for Antigravity CLI when running in Herdr.

Automatically injects real-time Herdr topology, sibling pane availability,
rate-limit safeguards, and task complexity model auto-switching rules into the agent's context.
"""

import json
import os
import sys

def emit_and_exit(data=None):
    if data is None:
        data = {}
    print(json.dumps(data))
    sys.exit(0)

# Gate: Only active inside Herdr
if os.environ.get("HERDR_ENV") != "1":
    emit_and_exit()

try:
    # Read payload from stdin as required by Antigravity hook protocol
    payload = {}
    try:
        if not sys.stdin.isatty():
            payload = json.load(sys.stdin)
    except Exception:
        pass

    ws_id = os.environ.get("HERDR_WORKSPACE_ID", "unknown")
    pane_id = os.environ.get("HERDR_PANE_ID", "unknown")

    # Construct context injection message
    msg = (
        f"[HERDR ACTIVE - Multi-Pane Orchestration & Adaptive Model Auto-Switching]\n"
        f"• Topology: Workspace={ws_id}, Orchestrator Pane={pane_id}\n"
        f"• Token Quota Protection: Delegate subtasks to sibling panes to conserve your tokens.\n"
        f"• Rate-Limit Mandate: ALWAYS run `herdr-orch check-limit <pane_id>` before delegating.\n"
        f"• Model Auto-Switching Guidelines by Task Complexity:\n"
        f"  - LOW (search, grep, read, lint, status, single test): gemini-3.8-flash-low (effort: low) | Subagent: flash_lite\n"
        f"  - MEDIUM (feature implementation, bug fixes, refactoring): gemini-3.8-flash-high | Subagent: flash / inherit\n"
        f"  - HIGH (system architecture, hard algorithms, security audit): gemini-3.1-pro-high | Subagent: pro\n"
        f"• CLI Helper: Use `herdr-orch status`, `herdr-orch check-limit`, `herdr-orch model-recommend`, and `herdr-orch delegate`."
    )

    emit_and_exit({
        "injectSteps": [
            {
                "ephemeralMessage": msg
            }
        ]
    })

except Exception:
    emit_and_exit()
