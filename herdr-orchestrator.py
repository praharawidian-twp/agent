#!/usr/bin/env python3
"""
herdr-orchestrator.py - Cross-Pane Orchestrator and Model Auto-Switching Utility for Herdr

Capabilities:
1. Discovers Herdr topology (current workspace, caller pane, sibling panes).
2. Performs Pre-flight Rate-Limit / Quota Checks on target panes before delegating.
3. Automatically classifies task complexity and recommends the optimal model (Flash-Low, Flash-High, Pro)
   to conserve token and quota usage.
4. Delegates tasks to available, non-limited worker panes.
5. Fetches and parses responses from worker panes for the orchestrator to synthesize.
6. Ensures worker panes exist (splitting panes on demand with --no-focus).
"""

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
import time
from typing import Any, Dict, List, Optional, Tuple

# Rate limit / Quota exhaustion indicators
RATE_LIMIT_PATTERNS = [
    r"resource[ _]exhausted",
    r"resource has been exhausted",
    r"rate[ _]?limit[ _]?(exceeded|reached)",
    r"429[ \t]+too many requests",
    r"quota[ _]?(exceeded|limit|exhausted)",
    r"exceeded your current quota",
    r"credit balance is too low",
    r"monthly limit reached",
    r"usage limit reached",
    r"capacity exhausted",
    r"overloaded with requests",
    r"daily limit reached",
    r"you have reached your limit",
    r"please wait until",
    r"billing account.*limit",
    r"insufficient[ _]?quota",
]

# Blocked / User Confirmation indicators
BLOCKED_PATTERNS = [
    r"Requesting permission for:",
    r"Run this command\?",
    r"approve\? \[[yY]/[nN]\]",
    r"Press enter to confirm",
    r"Do you want to proceed\?",
    r"Allow access to this URL\?",
    r"Allow access\?",
    r"> 1\. Yes",
    r"Yes, allow access",
    r"Yes, run command",
]

# Model recommendations per complexity tier
MODEL_TIERS = {
    "low": {
        "tier": "low",
        "label": "Simple / Light",
        "agy_model": "gemini-3.8-flash-low",
        "effort": "low",
        "subagent_model": "flash_lite",
        "token_economy": "Maximum token savings (~80-90% quota preserved)",
        "description": "Fast lookups, file grep, linting, simple regex, single unit test run, status checks."
    },
    "medium": {
        "tier": "medium",
        "label": "Moderate / Standard",
        "agy_model": "gemini-3.8-flash-high",
        "effort": "medium",
        "subagent_model": "flash",
        "token_economy": "Balanced high accuracy and token efficiency",
        "description": "Feature implementation, bug fixing, multi-file code review, standard refactoring."
    },
    "high": {
        "tier": "high",
        "label": "Complex / High-Reasoning",
        "agy_model": "gemini-3.1-pro-high",
        "effort": "high",
        "subagent_model": "pro",
        "token_economy": "Premium reasoning quota (use sparingly for difficult tasks)",
        "description": "Deep architecture design, complex algorithms, multi-system integration, security audits."
    }
}

LOW_COMPLEXITY_KEYWORDS = [
    "find", "search", "grep", "read", "view", "cat", "ls", "status", "git status",
    "git diff", "test single", "lint", "format", "check", "ping", "echo", "syntax",
    "simple", "trivial", "lookup", "count", "head", "tail",
    # Indonesian terms
    "cari", "temukan", "baca", "lihat", "cek", "periksa", "tampilkan", "hitung",
    "ringan", "mudah", "sederhana"
]

HIGH_COMPLEXITY_KEYWORDS = [
    "architecture", "redesign", "refactor entire", "security audit", "vulnerability",
    "complex algorithm", "concurrency", "distributed", "migration", "deep reasoning",
    "hard", "kernel", "cryptography", "distributed consensus", "benchmark optimization",
    # Indonesian terms
    "arsitektur", "desain ulang", "keamanan", "vulnerabilitas", "audit keamanan",
    "algoritma rumit", "konsensus", "distribusi", "migrasi arsitektur", "kompleks",
    "analisis mendalam", "skala besar"
]


def run_herdr_cmd(args: List[str], timeout: int = 15) -> Tuple[int, str, str]:
    """Execute a herdr CLI command and return (exit_code, stdout, stderr)."""
    cmd = ["herdr"] + args
    try:
        res = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=os.environ.copy()
        )
        return res.returncode, res.stdout.strip(), res.stderr.strip()
    except subprocess.TimeoutExpired:
        return 124, "", f"Command timed out after {timeout}s: {' '.join(cmd)}"
    except Exception as e:
        return 1, "", str(e)


def is_inside_herdr() -> bool:
    """Check whether the process is running inside Herdr."""
    return os.environ.get("HERDR_ENV") == "1"


def get_caller_pane_id() -> str:
    """Return the pane ID of the caller (orchestrator)."""
    return os.environ.get("HERDR_PANE_ID", "w1:p1")


def get_current_workspace_id() -> str:
    """Return the workspace ID of the caller."""
    return os.environ.get("HERDR_WORKSPACE_ID", "w1")


def check_pane_rate_limit(pane_id: str, lines: int = 80) -> Dict[str, Any]:
    """
    Inspect the latest terminal output of a pane to detect if it is currently
    rate-limited or exhausted, and if it is blocked on user permission.
    """
    code, stdout, stderr = run_herdr_cmd(["pane", "read", pane_id, "--source", "recent-unwrapped", "--lines", str(lines)])
    output_text = stdout if code == 0 else stderr

    is_limited = False
    limit_matches = []
    for pat in RATE_LIMIT_PATTERNS:
        match = re.search(pat, output_text, re.IGNORECASE)
        if match:
            is_limited = True
            limit_matches.append(match.group(0))

    is_blocked = False
    blocked_matches = []
    for pat in BLOCKED_PATTERNS:
        match = re.search(pat, output_text, re.IGNORECASE)
        if match:
            is_blocked = True
            blocked_matches.append(match.group(0))

    return {
        "pane_id": pane_id,
        "is_rate_limited": is_limited,
        "rate_limit_indicators": list(set(limit_matches)),
        "is_blocked": is_blocked,
        "blocked_indicators": list(set(blocked_matches)),
        "recent_snippet": "\n".join(output_text.splitlines()[-5:]) if output_text else ""
    }


def classify_task_complexity(task_text: str) -> Dict[str, Any]:
    """
    Classify the complexity of a task into low, medium, or high,
    and return the recommended model, effort, and token economy advice.
    """
    normalized = task_text.lower().strip()

    # Explicit override checks
    if normalized in ["low", "simple", "ringan"]:
        tier = "low"
        reason = "Explicit low/simple tier specified."
    elif normalized in ["medium", "moderate", "menengah", "standar"]:
        tier = "medium"
        reason = "Explicit medium tier specified."
    elif normalized in ["high", "complex", "kompleks", "berat"]:
        tier = "high"
        reason = "Explicit high/complex tier specified."
    else:
        # Heuristic scoring
        high_score = sum(1 for kw in HIGH_COMPLEXITY_KEYWORDS if kw in normalized)
        low_score = sum(1 for kw in LOW_COMPLEXITY_KEYWORDS if kw in normalized)

        # Length factor: very short single-line prompt with simple verb is likely low
        words = normalized.split()
        if len(words) <= 12 and low_score > 0 and high_score == 0:
            tier = "low"
            reason = f"Short task matching light keywords ({low_score} matched)."
        elif high_score > 0:
            tier = "high"
            reason = f"Task contains high-reasoning keywords ({high_score} matched)."
        elif low_score >= 2 and high_score == 0:
            tier = "low"
            reason = f"Task matches multiple lightweight keywords ({low_score} matched)."
        else:
            tier = "medium"
            reason = "Standard development task with balanced complexity."

    rec = MODEL_TIERS[tier].copy()
    rec["reason"] = reason
    rec["input_task"] = task_text
    return rec


def list_topology(workspace_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Discover all panes in the current workspace, check their health,
    agent status, process info, and rate-limit condition.
    """
    if not is_inside_herdr():
        return {
            "herdr_active": False,
            "error": "Not running inside a Herdr environment (HERDR_ENV is not set to 1)."
        }

    ws_id = workspace_id or get_current_workspace_id()
    caller_pane = get_caller_pane_id()

    # List panes
    code, stdout, _ = run_herdr_cmd(["pane", "list", "--workspace", ws_id])
    panes_data = []
    if code == 0:
        try:
            parsed = json.loads(stdout)
            panes_data = parsed.get("result", {}).get("panes", [])
        except Exception:
            pass

    # List agents
    code_ag, stdout_ag, _ = run_herdr_cmd(["agent", "list"])
    agents_map = {}
    if code_ag == 0:
        try:
            parsed_ag = json.loads(stdout_ag)
            for ag in parsed_ag.get("result", {}).get("agents", []):
                pid = ag.get("pane_id")
                if pid:
                    agents_map[pid] = ag
        except Exception:
            pass

    inspected_panes = []
    available_workers = []

    for p in panes_data:
        pid = p.get("pane_id")
        is_caller = (pid == caller_pane)
        agent_status = p.get("agent_status", "unknown")
        agent_type = p.get("agent", "none")

        # Check rate limit and blocked status
        limit_info = check_pane_rate_limit(pid, lines=60)
        is_limited = limit_info["is_rate_limited"]
        is_blocked = limit_info["is_blocked"]

        # Determine overall pane state
        if is_limited:
            state = "LIMITED"
        elif is_blocked:
            state = "BLOCKED"
        elif agent_status == "working":
            state = "BUSY"
        elif agent_status in ["idle", "done"]:
            state = "AVAILABLE"
        elif agent_status == "unknown":
            state = "SHELL_AVAILABLE"
        else:
            state = agent_status.upper()

        pane_entry = {
            "pane_id": pid,
            "is_orchestrator": is_caller,
            "state": state,
            "agent": agent_type,
            "agent_status": agent_status,
            "is_rate_limited": is_limited,
            "rate_limit_indicators": limit_info["rate_limit_indicators"],
            "is_blocked": is_blocked,
            "blocked_indicators": limit_info["blocked_indicators"],
            "cwd": p.get("cwd", ""),
            "snippet": limit_info["recent_snippet"]
        }
        inspected_panes.append(pane_entry)

        # Worker candidate: sibling pane, not caller, not limited, not busy, not blocked
        if not is_caller and not is_limited and not is_blocked and state in ["AVAILABLE", "SHELL_AVAILABLE"]:
            available_workers.append(pid)

    return {
        "herdr_active": True,
        "workspace_id": ws_id,
        "orchestrator_pane_id": caller_pane,
        "total_panes": len(inspected_panes),
        "available_workers": available_workers,
        "panes": inspected_panes
    }


def ensure_worker_pane(direction: str = "right", model: Optional[str] = None) -> Dict[str, Any]:
    """
    Ensure at least one worker pane exists in the current workspace.
    If no sibling pane is available, split the current pane with --no-focus.
    """
    topo = list_topology()
    if not topo.get("herdr_active"):
        return topo

    available = topo.get("available_workers", [])
    if available:
        return {
            "status": "existing_worker_available",
            "pane_id": available[0],
            "message": f"Worker pane {available[0]} is already available and ready."
        }

    # Split a new pane
    cwd = os.getcwd()
    cmd = ["pane", "split", "--current", "--direction", direction, "--cwd", cwd, "--no-focus"]
    code, stdout, stderr = run_herdr_cmd(cmd)
    if code != 0:
        return {
            "status": "error",
            "error": f"Failed to split pane: {stderr}"
        }

    new_pane_id = None
    try:
        parsed = json.loads(stdout)
        new_pane_id = parsed.get("result", {}).get("pane", {}).get("pane_id")
    except Exception:
        pass

    if not new_pane_id:
        # Fallback query topology to find newly added pane
        new_topo = list_topology()
        existing_ids = {p["pane_id"] for p in topo.get("panes", [])}
        for p in new_topo.get("panes", []):
            if p["pane_id"] not in existing_ids:
                new_pane_id = p["pane_id"]
                break

    # If model is requested, optionally initialize an agy-auto session in the new pane
    if new_pane_id and model:
        time.sleep(0.5)
        run_herdr_cmd(["pane", "send-text", new_pane_id, f"agy-auto --model {model}\n"])

    return {
        "status": "created",
        "pane_id": new_pane_id,
        "direction": direction,
        "cwd": cwd,
        "message": f"Created new worker pane {new_pane_id} with direction {direction}."
    }


def delegate_task(
    target_pane: str,
    task_prompt: str,
    model: Optional[str] = None,
    timeout_ms: int = 120000,
    wait_settled: bool = True
) -> Dict[str, Any]:
    """
    Delegate a task to a target pane:
    1. Verify target pane is NOT the orchestrator pane.
    2. Check target pane rate-limit status. If limited, ABORT immediately.
    3. Check if target pane is blocked on permission. If blocked, report error.
    4. Send task prompt to target.
    5. Optionally wait for completion and fetch output.
    """
    caller_pane = get_caller_pane_id()
    if target_pane == caller_pane:
        return {
            "status": "error",
            "error": f"Cannot delegate task to orchestrator's own pane ({target_pane}). Specify a sibling worker pane."
        }

    # Pre-flight Rate Limit Check
    limit_check = check_pane_rate_limit(target_pane, lines=80)
    if limit_check["is_rate_limited"]:
        return {
            "status": "rejected_rate_limited",
            "pane_id": target_pane,
            "error": f"Target pane {target_pane} is currently RATE-LIMITED or OUT OF QUOTA! Task delegation aborted to protect token economy.",
            "indicators": limit_check["rate_limit_indicators"]
        }

    if limit_check["is_blocked"]:
        return {
            "status": "rejected_blocked",
            "pane_id": target_pane,
            "error": f"Target pane {target_pane} is BLOCKED waiting for interactive input or approval.",
            "indicators": limit_check["blocked_indicators"]
        }

    marker_id = f"TASK_{int(time.time())}"
    decorated_prompt = (
        f"# [HERDR-DELEGATED TASK {marker_id}]\n"
        f"{task_prompt}\n"
    )

    code_ag, stdout_ag, _ = run_herdr_cmd(["agent", "get", target_pane])
    has_agent = (code_ag == 0)

    if has_agent:
        args = ["agent", "prompt", target_pane, decorated_prompt]
        if wait_settled:
            args += ["--wait", "--timeout", str(timeout_ms)]
        code, stdout, stderr = run_herdr_cmd(args, timeout=(timeout_ms // 1000) + 10)
        if code != 0:
            return {
                "status": "agent_prompt_failed",
                "pane_id": target_pane,
                "error": stderr or stdout
            }
        code_r, stdout_r, _ = run_herdr_cmd(["agent", "read", target_pane, "--source", "recent-unwrapped", "--lines", "100"])
        return {
            "status": "success",
            "pane_id": target_pane,
            "delivery": "agent_prompt",
            "marker_id": marker_id,
            "output": stdout_r
        }
    else:
        if model:
            run_cmd = f"agy-auto --model {model} -p {shlex.quote(task_prompt)}"
            code, stdout, stderr = run_herdr_cmd(["pane", "run", target_pane, run_cmd])
        else:
            code, stdout, stderr = run_herdr_cmd(["pane", "send-text", target_pane, f"{task_prompt}\n"])

        if code != 0:
            return {
                "status": "pane_send_failed",
                "pane_id": target_pane,
                "error": stderr or stdout
            }

        time.sleep(1.0)
        code_r, stdout_r, _ = run_herdr_cmd(["pane", "read", target_pane, "--source", "recent-unwrapped", "--lines", "60"])
        return {
            "status": "success",
            "pane_id": target_pane,
            "delivery": "pane_run",
            "marker_id": marker_id,
            "output": stdout_r
        }


def fetch_pane_output(target_pane: str, lines: int = 100) -> Dict[str, Any]:
    """Fetch recent unwrapped terminal or agent output from target pane."""
    code_ag, stdout_ag, _ = run_herdr_cmd(["agent", "read", target_pane, "--source", "recent-unwrapped", "--lines", str(lines)])
    if code_ag == 0 and stdout_ag:
        return {
            "status": "success",
            "pane_id": target_pane,
            "source": "agent_read",
            "output": stdout_ag
        }

    code_p, stdout_p, stderr_p = run_herdr_cmd(["pane", "read", target_pane, "--source", "recent-unwrapped", "--lines", str(lines)])
    if code_p == 0:
        return {
            "status": "success",
            "pane_id": target_pane,
            "source": "pane_read",
            "output": stdout_p
        }
    return {
        "status": "error",
        "pane_id": target_pane,
        "error": stderr_p
    }


def run_orchestrated_task(
    task_prompt: str,
    complexity: Optional[str] = None,
    preferred_pane: Optional[str] = None,
    timeout_ms: int = 120000
) -> Dict[str, Any]:
    """
    End-to-end Orchestrated Pipeline:
    1. Classifies task complexity and selects optimal model (auto-switch).
    2. Identifies or creates a non-limited available worker pane.
    3. Delegates the task.
    4. Fetches the clean result and returns structured output.
    """
    model_info = classify_task_complexity(complexity or task_prompt)
    chosen_model = model_info["agy_model"]

    topo = list_topology()
    if not topo.get("herdr_active"):
        return {
            "status": "error",
            "error": topo.get("error", "Herdr is not active.")
        }

    target_pane = preferred_pane
    if not target_pane:
        available_workers = topo.get("available_workers", [])
        if available_workers:
            target_pane = available_workers[0]
        else:
            res_worker = ensure_worker_pane(direction="right")
            if res_worker.get("status") in ["created", "existing_worker_available"]:
                target_pane = res_worker.get("pane_id")
            else:
                return {
                    "status": "error",
                    "error": f"Failed to obtain an available worker pane: {res_worker}"
                }

    del_res = delegate_task(
        target_pane=target_pane,
        task_prompt=task_prompt,
        model=chosen_model,
        timeout_ms=timeout_ms,
        wait_settled=True
    )

    return {
        "status": del_res.get("status"),
        "orchestrator_pane": topo.get("orchestrator_pane_id"),
        "worker_pane": target_pane,
        "model_selection": model_info,
        "delegation_result": del_res
    }


def main():
    parser = argparse.ArgumentParser(
        description="herdr-orchestrator: Cross-pane task orchestrator and adaptive model switcher for Herdr."
    )
    subparsers = parser.add_subparsers(dest="command", help="Subcommand to execute")

    # status
    p_status = subparsers.add_parser("status", help="Inspect Herdr topology, sibling panes, and rate-limit states.")
    p_status.add_argument("--json", action="store_true", help="Output raw JSON")

    # check-limit
    p_chk = subparsers.add_parser("check-limit", help="Verify whether a pane is currently rate-limited or out of quota.")
    p_chk.add_argument("pane_id", help="Target pane ID (e.g. w1:p4)")
    p_chk.add_argument("--lines", type=int, default=80, help="Number of recent lines to inspect")

    # model-recommend
    p_mod = subparsers.add_parser("model-recommend", help="Classify task complexity and recommend optimal model.")
    p_mod.add_argument("task", help="Task description or complexity tag (low/medium/high)")

    # delegate
    p_del = subparsers.add_parser("delegate", help="Delegate a task to a non-limited worker pane.")
    p_del.add_argument("pane_id", help="Target worker pane ID")
    p_del.add_argument("prompt", help="Task prompt to send")
    p_del.add_argument("--model", help="Optional model name override (e.g. gemini-3.8-flash-low)")
    p_del.add_argument("--timeout", type=int, default=120000, help="Timeout in ms (default 120000)")

    # fetch
    p_fetch = subparsers.add_parser("fetch", help="Fetch output from target pane.")
    p_fetch.add_argument("pane_id", help="Target pane ID")
    p_fetch.add_argument("--lines", type=int, default=100, help="Number of lines to read")

    # ensure-worker
    p_ens = subparsers.add_parser("ensure-worker", help="Ensure an available worker pane exists.")
    p_ens.add_argument("--direction", default="right", choices=["right", "down"])
    p_ens.add_argument("--model", help="Optional model to launch in new worker pane")

    # run-task
    p_run = subparsers.add_parser("run-task", help="Auto-classify complexity, pick model, delegate to available pane, and fetch response.")
    p_run.add_argument("prompt", help="Task prompt")
    p_run.add_argument("--complexity", choices=["low", "medium", "high"], help="Explicit complexity level")
    p_run.add_argument("--pane", help="Preferred worker pane ID")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "status":
        res = list_topology()
        if getattr(args, "json", False):
            print(json.dumps(res, indent=2))
        else:
            if not res.get("herdr_active"):
                print(f"[!] {res.get('error')}")
                sys.exit(1)
            print(f"=== HERDR ORCHESTRATOR STATUS ===")
            print(f"Workspace: {res['workspace_id']} | Orchestrator Pane: {res['orchestrator_pane_id']}")
            print(f"Total Panes: {res['total_panes']} | Available Non-Limited Workers: {res['available_workers']}\n")
            for p in res["panes"]:
                role = " [ORCHESTRATOR]" if p["is_orchestrator"] else " [WORKER]"
                lim_tag = " [RATE-LIMITED!]" if p["is_rate_limited"] else ""
                blk_tag = " [BLOCKED!]" if p["is_blocked"] else ""
                print(f"- Pane {p['pane_id']}{role}: State={p['state']}, Agent={p['agent']} ({p['agent_status']}){lim_tag}{blk_tag}")
                if p["rate_limit_indicators"]:
                    print(f"  * Rate Limit Indicators: {p['rate_limit_indicators']}")
                if p["is_blocked"]:
                    print(f"  * Blocked Indicators: {p['blocked_indicators']}")

    elif args.command == "check-limit":
        res = check_pane_rate_limit(args.pane_id, lines=args.lines)
        print(json.dumps(res, indent=2))

    elif args.command == "model-recommend":
        res = classify_task_complexity(args.task)
        print(json.dumps(res, indent=2))

    elif args.command == "delegate":
        res = delegate_task(args.pane_id, args.prompt, model=args.model, timeout_ms=args.timeout)
        print(json.dumps(res, indent=2))

    elif args.command == "fetch":
        res = fetch_pane_output(args.pane_id, lines=args.lines)
        if res.get("status") == "success":
            print(res.get("output", ""))
        else:
            print(json.dumps(res, indent=2))

    elif args.command == "ensure-worker":
        res = ensure_worker_pane(direction=args.direction, model=args.model)
        print(json.dumps(res, indent=2))

    elif args.command == "run-task":
        res = run_orchestrated_task(args.prompt, complexity=args.complexity, preferred_pane=args.pane)
        print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
