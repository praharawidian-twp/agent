#!/usr/bin/env bash
set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}================================================================${NC}"
echo -e "${BLUE}  🚀 Antigravity Autonomous Multi-Agent Framework Installer     ${NC}"
echo -e "${BLUE}================================================================${NC}"

echo -e "\n[*] Checking prerequisites..."
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}[!] Python 3 not found. Please install Python 3.8+ first.${NC}"
    exit 1
fi
PY_VER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo -e "${GREEN}[✓] Python 3 detected: ${PY_VER}${NC}"

INSTALL_DIR="${HOME}/.gemini/team-orch"
LOCAL_BIN="${HOME}/.local/bin"
SKILL_DIR="${HOME}/.gemini/config/skills/team-orchestrator"
GLOBAL_RULES="${HOME}/.gemini/GEMINI.md"

echo -e "\n[*] Setting up directories..."
mkdir -p "${INSTALL_DIR}/roles" "${INSTALL_DIR}/templates" "${INSTALL_DIR}/docs" "${INSTALL_DIR}/scripts"
mkdir -p "${LOCAL_BIN}"
mkdir -p "${SKILL_DIR}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo -e "[*] Installing roles, templates, and utilities..."
if [ -d "${REPO_DIR}/.agents/roles" ]; then
    cp -r "${REPO_DIR}/.agents/roles/"* "${INSTALL_DIR}/roles/"
fi
if [ -d "${REPO_DIR}/.agents/templates" ]; then
    cp -r "${REPO_DIR}/.agents/templates/"* "${INSTALL_DIR}/templates/"
fi
if [ -d "${REPO_DIR}/.agents/docs" ]; then
    cp -r "${REPO_DIR}/.agents/docs/"* "${INSTALL_DIR}/docs/"
fi

echo -e "[*] Installing CLI tools into ${LOCAL_BIN}..."
cp "${REPO_DIR}/.agents/scripts/team-orch" "${INSTALL_DIR}/team-orch"
chmod +x "${INSTALL_DIR}/team-orch"
ln -sf "${INSTALL_DIR}/team-orch" "${LOCAL_BIN}/team-orch"

if [ -f "${REPO_DIR}/herdr-orchestrator.py" ]; then
    cp "${REPO_DIR}/herdr-orchestrator.py" "${INSTALL_DIR}/herdr-orchestrator.py"
    chmod +x "${INSTALL_DIR}/herdr-orchestrator.py"
    ln -sf "${INSTALL_DIR}/herdr-orchestrator.py" "${LOCAL_BIN}/herdr-orch"
fi

echo -e "[*] Installing global rules & skills..."
if [ -f "${REPO_DIR}/GEMINI.md" ]; then
    cp "${REPO_DIR}/GEMINI.md" "${GLOBAL_RULES}"
fi

cat << 'EOF' > "${SKILL_DIR}/SKILL.md"
---
name: team-orchestrator
description: Autonomous Multi-Agent Team Orchestrator (PM, Senior Lead Engineer/Analis, Coder, Dokumenter). Use when managing multi-agent software engineering workflows, Herdr cross-pane task delegation, strict gatekeeper code reviews, read-only Git policy, and transparent audit trails.
---

# Autonomous Multi-Agent Team Orchestration

Sistem orkestrator tim rekayasa perangkat lunak otonom terintegrasi dengan Herdr multi-pane dan Antigravity.

---

## 1. Peran Tim & Hierarki

1. **Project Manager (PM)** (`gemini-3.8-flash-high`):
   - **Komunikasi Manusia**: Berdialog dengan pengguna dalam bahasa manusia yang ramah, ringkas, dan empatik.
   - **Proactive Clarification**: Dilarang berasumsi. Jika ada ambiguitas logika bisnis atau batasan sistem, PM wajib bertanya balik ke Pengguna sebelum menyusun dokumen kebutuhan.
   - **Output**: `tasks/<project_id>/01-requirements.md` (Wajib persetujuan Pengguna / Approval Gate).

2. **Analis / Senior Lead Engineer (Tech Lead)** (`gemini-3.1-pro-high`):
   - **Audit Boilerplate**: Menyelidiki struktur direktori, konvensi penamaan, dan utilitas yang sudah ada di repositori sebelum merancang kode baru.
   - **Technical Stewardship**: Menjaga Clean Code, keamanan (no hardcoded secrets, input sanitasi), prinsip SOLID, dan performa.
   - **Bukan Sekadar Tes Hijau**: Unit test adalah syarat minimal, Analis wajib menilai kualitas kode dan kesesuaian kebutuhan.
   - **Output**: `02-technical-spec.md`, `03-task-list.md`, dan `review-log.md`.

3. **Coder (Software Developer)** (`gemini-3.8-flash-high`):
   - Mengimplementasikan sub-task atomik sesuai spesifikasi teknis.
   - Wajib menyertakan unit test menyeluruh dan menjalankannya sampai 100% *PASS*.
   - Tidak boleh memodifikasi Git (`git add`, `git commit`, `git push` dilarang).

4. **Dokumenter** (`gemini-3.8-flash-low`):
   - Menyusun dokumentasi teknis dan panduan pemakaian di folder `docs/`.

---

## 2. Aturan Baku Sistem

1. **Git Policy (CRITICAL - Read-Only)**:
   - Seluruh agen DILARANG menjalankan `git add`, `git commit`, `git push`, `git merge`, dll.
   - Hanya operasi inspeksi yang diperbolehkan (`git status`, `git diff`, `git log`).
2. **Audit Trail Mandatori**:
   - Seluruh tindakan teknis dan verifikasi keamanan wajib dicatat di `tasks/<project_id>/audit-trail.md` melalui `team-orch log`.
   - Setiap agen wajib mengamati log audit sebelumnya sebelum bertindak untuk mencegah regresi/anomali.
3. **Pustaka Reusable Scripts**:
   - Skrip otomasi yang bermanfaat disimpan secara permanen di `.agents/scripts/` (atau `~/.gemini/team-orch/scripts/`), bukan skrip sekali-pakai (*scratch script*), untuk menghemat hingga 90% kuota token.

---

## 3. Perintah CLI Utama (`team-orch`)

```bash
# Global Mission Control Dashboard (Multi-project & Worker Fleet)
team-orch status

# Status detail proyek tertentu
team-orch status <project_id>

# Mulai proyek baru
team-orch init <project_id>

# User Approval Gate
team-orch approve <project_id>

# Lihat riwayat audit trail transparan
team-orch audit <project_id> [-n 10]

# Catat aksi ke audit trail
team-orch log <project_id> -r <role> -e <event> -d "<deskripsi>"

# Generate prompt peran lengkap
team-orch prompt <role> <project_id>

# Delegasikan ke Herdr worker pane
team-orch dispatch <role> <project_id> --pane <pane_id>

# Arsipkan proyek yang tuntas
team-orch complete <project_id>
```
EOF


echo -e "\n${GREEN}================================================================${NC}"
echo -e "${GREEN}  🎉 Installation Complete! All agents are ready to serve.     ${NC}"
echo -e "${GREEN}================================================================${NC}"
echo -e "Try running: ${YELLOW}team-orch status${NC}"
