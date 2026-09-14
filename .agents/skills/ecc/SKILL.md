---
name: ecc
description: The Everything Claude Code (ECC) harness performance optimization system. Use this skill when the user asks about ECC capabilities, wants to apply ECC workflows (verification loops, TDD, strategic compact, context budget, unified memory, rules distillation, security reviews), or navigate ECC skills, recipes, and documentation in Antigravity.
---

# Everything Claude Code (ECC) in Antigravity

**ECC (Everything Claude Code / ECC Universal)** is an open-source agent harness performance optimization system. It provides structured workflows, memory mechanisms, instincts, security patterns, and research-first engineering practices adapted for AI agents (Antigravity `agy`, Claude Code, Codex, Cursor).

---

## 1. Quick Navigation & Sub-Skills

ECC in this workspace is organized modularly using progressive disclosure:

| Skill / Reference | Path | Focus |
| :--- | :--- | :--- |
| **ECC Guide** | [SKILL.md](../ecc-guide/SKILL.md) | Navigation, components catalog, install profiles, and onboarding. |
| **ECC Recipes** | [SKILL.md](../ecc-recipes/SKILL.md) | Step-by-step recipes and workflows for common dev tasks. |
| **Commands Quick Reference** | [COMMANDS-QUICK-REF.md](./references/COMMANDS-QUICK-REF.md) | Quick cheat sheet of commands, subagents, and workflows. |
| **Shortform Guide** | [the-shortform-guide.md](./references/the-shortform-guide.md) | Compact guide to ECC architecture, rules, and agents. |
| **Security Guide** | [the-security-guide.md](./references/the-security-guide.md) | Security scan, prompt-injection defense, dependency audit. |
| **Longform Guide** | [the-longform-guide.md](./references/the-longform-guide.md) | In-depth breakdown of the full ECC ecosystem and mechanics. |

---

## 2. Core ECC Workflows & Principles

When applying ECC methodologies in Antigravity pair-programming:

### A. Verification Loop & TDD
1. **Write or confirm tests first**: Before implementing feature logic, define unit/integration tests establishing expected inputs/outputs.
2. **Deterministic verification**: Never mark a task complete without executing tests, linters, or type checks.
3. **Loop until green**: Iterate on error output until all validation criteria pass.

### B. Token Economy & Context Budget
1. **Progressive Disclosure**: Keep prompt context lean. Load references only when needed.
2. **Strategic Compact**: Summarize findings and prune stale command logs before delegating or continuing lengthy sessions.
3. **Model Auto-Switching**: When operating inside Herdr orchestrator or Antigravity, reserve `pro` models for high-complexity architecture while using `flash` models for lookups and edits.

### C. Security-First Development
1. **Dependency & Prompt-Injection Auditing**: Scan external inputs and packages before installation.
2. **Least Privilege**: Verify tool execution and avoid indiscriminate destructive operations.
3. **Deterministic Sandbox**: Validate changes in isolated subagents or branches before merging into main.

---

## 3. Recommended Subagent Delegation Patterns

ECC emphasizes specialized subagent roles for complex workflows:
- **`research`**: Read-only codebase explorer for scanning dependencies, APIs, and project architecture.
- **`reviewer`**: Targeted code review checking security, edge cases, and coding conventions.
- **`worker`**: Atomic task execution (implementing a single function, writing test cases).

---

## 4. Verification Checklist

Before finishing any task driven by ECC:
- [ ] Requirements verified against existing codebase conventions.
- [ ] Code edits verified with compiler, linter, or test suite.
- [ ] Stale or sensitive temporary files cleaned up.
- [ ] Clear, concise summary provided to the user.
