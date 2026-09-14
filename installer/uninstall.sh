#!/usr/bin/env bash
set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${RED}================================================================${NC}"
echo -e "${RED}  🗑️  Autonomous Multi-Agent Framework - Clean Uninstaller     ${NC}"
echo -e "${RED}================================================================${NC}"
echo -e "Skrip ini akan menghapus instalasi global framework dari perangkat ini.\n"

INSTALL_DIR="${HOME}/.gemini/team-orch"
LOCAL_BIN="${HOME}/.local/bin"
SKILL_DIR="${HOME}/.gemini/config/skills/team-orchestrator"
GLOBAL_RULES="${HOME}/.gemini/GEMINI.md"
HERDR_CONFIG="${HOME}/.config/herdr/config.toml"

# 1. Hapus symlinks CLI
echo -e "[*] Menghapus symlink CLI dari ${LOCAL_BIN}..."
if [ -L "${LOCAL_BIN}/team-orch" ] || [ -f "${LOCAL_BIN}/team-orch" ]; then
    rm -f "${LOCAL_BIN}/team-orch"
    echo -e "${GREEN}[✓] Dihapus: ${LOCAL_BIN}/team-orch${NC}"
fi

if [ -L "${LOCAL_BIN}/herdr-orch" ] || [ -f "${LOCAL_BIN}/herdr-orch" ]; then
    rm -f "${LOCAL_BIN}/herdr-orch"
    echo -e "${GREEN}[✓] Dihapus: ${LOCAL_BIN}/herdr-orch${NC}"
fi

# 2. Hapus direktori global store
echo -e "\n[*] Menghapus direktori data global ${INSTALL_DIR}..."
if [ -d "${INSTALL_DIR}" ]; then
    rm -rf "${INSTALL_DIR}"
    echo -e "${GREEN}[✓] Dihapus: ${INSTALL_DIR}${NC}"
else
    echo -e "${BLUE}[-] Tidak ditemukan: ${INSTALL_DIR}${NC}"
fi

# 3. Hapus custom skill
echo -e "\n[*] Menghapus skill team-orchestrator..."
if [ -d "${SKILL_DIR}" ]; then
    rm -rf "${SKILL_DIR}"
    echo -e "${GREEN}[✓] Dihapus: ${SKILL_DIR}${NC}"
else
    echo -e "${BLUE}[-] Tidak ditemukan: ${SKILL_DIR}${NC}"
fi

# 4. Tangani global rules di GEMINI.md
echo -e "\n[*] Menangani aturan global di ${GLOBAL_RULES}..."
if [ -f "${GLOBAL_RULES}" ]; then
    BACKUP_RULES="${GLOBAL_RULES}.bak.$(date +%Y%m%d%H%M%S)"
    mv "${GLOBAL_RULES}" "${BACKUP_RULES}"
    echo -e "${GREEN}[✓] File aturan global dicadangkan ke: ${BACKUP_RULES}${NC}"
    echo -e "${YELLOW}[!] Catatan: File asli ${GLOBAL_RULES} telah dinonaktifkan.${NC}"
fi

# 5. Konfigurasi Herdr (opsional)
echo -e "\n[*] Memeriksa konfigurasi Herdr (${HERDR_CONFIG})..."
if [ -f "${HERDR_CONFIG}" ]; then
    echo -e "${BLUE}[i] File konfigurasi Herdr tetap dipertahankan di: ${HERDR_CONFIG}${NC}"
    echo -e "    Jika ingin menghapus manual: rm -f ${HERDR_CONFIG}"
fi

echo -e "\n${GREEN}================================================================${NC}"
echo -e "${GREEN}  ✨ Uninstallation Selesai! Framework berhasil dibersihkan.    ${NC}"
echo -e "${GREEN}================================================================${NC}"
echo -e "Perangkat Anda sekarang bersih dari konfigurasi global framework ini."
