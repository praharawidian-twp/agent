#!/usr/bin/env bash
set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=== VERIFIKASI SETUP FRAMEWORK MULTI-AGEN ===${NC}"

FAIL=0

# 1. Check team-orch CLI
if command -v team-orch &> /dev/null; then
    echo -e "${GREEN}[PASS] team-orch CLI:${NC} $(which team-orch)"
else
    echo -e "${RED}[FAIL] team-orch CLI tidak ditemukan di PATH (${HOME}/.local/bin).${NC}"
    FAIL=1
fi

# 2. Check herdr-orch CLI
if command -v herdr-orch &> /dev/null; then
    echo -e "${GREEN}[PASS] herdr-orch CLI:${NC} $(which herdr-orch)"
else
    echo -e "${RED}[FAIL] herdr-orch CLI tidak ditemukan di PATH (${HOME}/.local/bin).${NC}"
    FAIL=1
fi

# 3. Check uninstaller
if [ -f "${HOME}/.local/bin/team-orch-uninstall" ] || [ -f "$(dirname "$0")/uninstall.sh" ]; then
    echo -e "${GREEN}[PASS] Skrip Pembersih (Uninstaller):${NC} Siap digunakan"
else
    echo -e "${YELLOW}[WARN] Skrip uninstall belum terdaftar di PATH.${NC}"
fi

# 4. Check global store (roles & templates)
ROLE_COUNT=$(ls -1 "${HOME}/.gemini/team-orch/roles"/*.md 2>/dev/null | wc -l | tr -d ' ')
TMPL_COUNT=$(ls -1 "${HOME}/.gemini/team-orch/templates"/*.md 2>/dev/null | wc -l | tr -d ' ')

if [ "${ROLE_COUNT}" -ge 4 ] && [ "${TMPL_COUNT}" -ge 5 ]; then
    echo -e "${GREEN}[PASS] Global roles (${ROLE_COUNT}) & templates (${TMPL_COUNT}) di ~/.gemini/team-orch/${NC}"
else
    echo -e "${RED}[FAIL] Berkas peran atau template di ~/.gemini/team-orch/ tidak lengkap.${NC}"
    FAIL=1
fi

# 5. Check global skill
if [ -f "${HOME}/.gemini/config/skills/team-orchestrator/SKILL.md" ]; then
    echo -e "${GREEN}[PASS] Global skill terdaftar:${NC} ~/.gemini/config/skills/team-orchestrator/SKILL.md"
else
    echo -e "${RED}[FAIL] Global skill team-orchestrator tidak ditemukan.${NC}"
    FAIL=1
fi

# 6. Check global rules
if grep -q "Strict Git Policy" "${HOME}/.gemini/GEMINI.md" 2>/dev/null; then
    echo -e "${GREEN}[PASS] Aturan global (Git Read-Only, Tech Lead, dll) aktif di ~/.gemini/GEMINI.md${NC}"
else
    echo -e "${RED}[FAIL] Aturan Strict Git Policy tidak ditemukan di ~/.gemini/GEMINI.md.${NC}"
    FAIL=1
fi

# 7. Check Herdr status
if command -v herdr &> /dev/null; then
    echo -e "${GREEN}[PASS] Herdr terminal manager:${NC} $(herdr --version 2>/dev/null || echo 'terpasang')"
else
    echo -e "${YELLOW}[INFO] Herdr belum terpasang (Opsional, diperlukan jika menggunakan multi-pane Herdr).${NC}"
fi

echo -e "${BLUE}=============================================${NC}"

if [ "${FAIL}" -eq 0 ]; then
    echo -e "${GREEN}[ALL CHECKS PASSED - FRAMEWORK SIAP DIGUNAKAN DI SEMUA PERANGKAT]${NC}"
    exit 0
else
    echo -e "${RED}[BEBERAPA PEMERIKSAAN GAGAL - SILAKAN JALANKAN ULANG ./installer/install.sh]${NC}"
    exit 1
fi
