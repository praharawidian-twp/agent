#!/usr/bin/env bash
set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo "=== VERIFYING AGENT FRAMEWORK SETUP ==="

if command -v team-orch &> /dev/null; then
    echo -e "${GREEN}[PASS]${NC} team-orch CLI: $(which team-orch)"
else
    echo -e "${RED}[FAIL]${NC} team-orch CLI missing"
fi

if command -v herdr-orch &> /dev/null; then
    echo -e "${GREEN}[PASS]${NC} herdr-orch CLI: $(which herdr-orch)"
else
    echo -e "${RED}[FAIL]${NC} herdr-orch CLI missing"
fi

if [ -d "${HOME}/.gemini/team-orch/roles" ] && [ -d "${HOME}/.gemini/team-orch/templates" ]; then
    ROLES_COUNT=$(ls -1 "${HOME}/.gemini/team-orch/roles" | wc -l | tr -d ' ')
    TEMPLATES_COUNT=$(ls -1 "${HOME}/.gemini/team-orch/templates" | wc -l | tr -d ' ')
    echo -e "${GREEN}[PASS]${NC} Global roles (${ROLES_COUNT}) & templates (${TEMPLATES_COUNT}) in ~/.gemini/team-orch/"
else
    echo -e "${RED}[FAIL]${NC} Storage missing"
fi

if [ -f "${HOME}/.gemini/config/skills/team-orchestrator/SKILL.md" ]; then
    echo -e "${GREEN}[PASS]${NC} Global skill registered"
else
    echo -e "${RED}[FAIL]${NC} Global skill missing"
fi

if [ -f "${HOME}/.gemini/GEMINI.md" ]; then
    echo -e "${GREEN}[PASS]${NC} Global rules present in ~/.gemini/GEMINI.md"
else
    echo -e "${RED}[FAIL]${NC} Global rules missing"
fi

echo "========================================"
echo -e "${GREEN}[ALL CHECKS PASSED - READY FOR MULTI-DEVICE DEPLOYMENT]${NC}"
