---
name: herdr-orchestrator
description: Orchestrate tasks across Herdr terminal panes and automatically adapt/switch model tiers based on task complexity to prevent token quota exhaustion. Use when running inside Herdr (HERDR_ENV=1), coordinating sibling terminal panes, delegating tasks, verifying pane rate limits, or auto-switching models (flash-low for simple tasks, flash-high for standard, pro for complex).
---

# Herdr Multi-Pane Orchestrator & Adaptive Model Auto-Switcher

This skill empowers Antigravity to act as a central **Orchestrator** across terminal panes inside [Herdr](https://herdr.dev). It distributes workload across available sibling panes in the same workspace to preserve token limits, ensures worker panes are not rate-limited before assigning tasks, and dynamically routes/switches models based on task complexity.

---

## 1. Core Principles

1. **Token & Quota Economy**:
   - Do not perform heavyweight, repetitive, or isolated subtasks solely within the main orchestrator conversation.
   - Offload secondary tasks (file lookups, test execution, linters, sub-module implementations) to sibling panes or dedicated worker agents.
2. **Mandatory Rate-Limit Pre-flight Check**:
   - **Never** delegate a task blindly.
   - Always run `herdr-orch check-limit <pane_id>` before assigning work to ensure the target pane is neither rate-limited (`429`, `RESOURCE_EXHAUSTED`, `quota exceeded`) nor blocked waiting on interactive approvals.
3. **Adaptive Model Selection (Auto-Switching)**:
   - Match model capability and reasoning effort to task complexity. Never use high-tier models for simple tasks.
4. **Result Synthesis**:
   - As Orchestrator, collect outputs from delegated panes, verify accuracy, handle edge cases, and present a coherent, final response to the user.

---

## 2. Model Auto-Switching Matrix

Evaluate every task before execution or delegation:

| Complexity Tier | Characteristics & Task Types | Target Model (`agy`) | Effort | Subagent Model (`invoke_subagent`) | Token Economy Impact |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **LOW (Simple)** | Grep, file lookups, log reads, git status/diff, syntax checks, single unit test runs, code formatting, health checks. | `gemini-3.8-flash-low` | `low` | `flash_lite` or `flash` | **~85-90% quota savings**. Minimal tokens, fastest response. |
| **MEDIUM (Standard)** | Feature implementation, bug fixes, multi-file code review, unit test authoring, standard refactoring. | `gemini-3.8-flash-high` / `claude-sonnet-4-6` | `medium` | `flash` or `inherit` | Balanced accuracy and token consumption. |
| **HIGH (Complex)** | System architecture redesign, multi-repo distributed logic, security vulnerability audits, deep mathematical/algorithmic reasoning. | `gemini-3.1-pro-high` / `claude-opus-4-6-thinking` | `high` | `pro` | Premium reasoning tokens. Use selectively. |

To automatically classify any prompt:
```bash
herdr-orch model-recommend "<task prompt or description>"
```

---

## 3. Workflow & Procedures

### Step 1: Discover Environment & Topology
Verify that you are in Herdr and inspect active panes:
```bash
herdr-orch status
```
Inspect the output:
- `Orchestrator Pane`: Your current pane (e.g. `w1:p1`). Never delegate to your own pane.
- `Available Non-Limited Workers`: Panes ready to receive tasks.
- `State`: `AVAILABLE`, `BUSY` (running), `BLOCKED` (waiting for user permission), or `LIMITED` (quota exhausted).

### Step 2: Ensure an Available Worker Pane Exists
If no sibling worker pane is free or available:
```bash
herdr-orch ensure-worker --direction right
```
This splits a sibling pane in the background (`--no-focus`) preserving the current working directory.

### Step 3: Verify Rate-Limit & Status (Mandatory)
Before delegating, verify target pane health:
```bash
herdr-orch check-limit <target_pane_id>
```
- If `"is_rate_limited": true`: **DO NOT DELEGATE**. Select another pane or run locally with a low-tier model.
- If `"is_blocked": true`: Inspect the pane prompt (`herdr-orch fetch <target_pane_id>`) and notify user if approval is needed.

### Step 4: Delegate the Task with Appropriate Model
Delegate the task using the recommended model:
```bash
# Example: Simple task delegated to w1:p4 with flash-low
herdr-orch delegate <target_pane_id> "Check git status and find all modified .py files" --model gemini-3.8-flash-low

# Or high-level end-to-end orchestration:
herdr-orch run-task "Run test suite on user auth module" --complexity medium
```

### Step 5: Fetch Response & Synthesize
Fetch the unwrapped output from the worker pane:
```bash
herdr-orch fetch <target_pane_id> --lines 80
```
Review the returned output, integrate the findings into your master plan, and provide the final synthesized response to the user.

---

## 4. CLI Quick Reference (`herdr-orch`)

- `herdr-orch status`: Full workspace topology and health check.
- `herdr-orch check-limit <pane>`: Inspects recent pane lines for quota/rate limit errors and blocked prompts.
- `herdr-orch model-recommend "<task>"`: Suggests tier, model, and effort for a given task.
- `herdr-orch delegate <pane> "<prompt>" [--model <model>] [--timeout <ms>]`: Safely dispatches task to worker pane.
- `herdr-orch fetch <pane> [--lines <n>]`: Reads clean unwrapped response from worker pane.
- `herdr-orch ensure-worker [--direction right|down]`: Splits new sibling pane if needed.
- `herdr-orch run-task "<prompt>" [--complexity low|medium|high]`: Automated end-to-end dispatch.
