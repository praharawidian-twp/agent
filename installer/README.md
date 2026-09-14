# 📦 Panduan Instalasi & Pembersihan (Installer & Uninstaller)

Direktori ini menyediakan skrip otomatisasi untuk memasang (*install*), memverifikasi (*verify*), dan membersihkan (*uninstall*) framework multi-agen otonom pada sistem operasi macOS atau Linux.

---

## 🚀 1. Pemasangan di Device Baru (Pilih Salah Satu)

### Cara A: 1-Prompt Setup Lewat Agen AI (Paling Praktis)
Jika Anda membuka Antigravity IDE atau Antigravity CLI (`agy`) di komputer baru, Anda cukup memberikan instruksi berikut ke agen:

> **Prompt ke AI Agen:**  
> *"Tolong terapkan dan pasang autonomous multi-agent framework dari repositori ini: https://github.com/praharawidian-twp/agent/tree/v0.1.0"*

Agen AI akan secara otomatis:
1. Meng-clone repositori (atau mengambil branch `v0.1.0`).
2. Menjalankan `./installer/install.sh`.
3. Memastikan konfigurasi Herdr (`~/.config/herdr/config.toml`) siap.
4. Menjalankan `./installer/verify.sh` untuk memastikan seluruh agen (PM, Analis, Coder, Dokumenter) aktif.

---

### Cara B: Pemasangan Manual via Terminal
Jalankan langkah berikut di terminal laptop/komputer baru Anda:

```bash
# 1. Clone repositori branch v0.1.0
git clone -b v0.1.0 https://github.com/praharawidian-twp/agent.git agent-framework
cd agent-framework

# 2. Jalankan skrip instalasi
./installer/install.sh

# 3. Jalankan verifikasi
./installer/verify.sh
```

---

## 🔍 2. Apa Saja yang Dikonfigurasi oleh `install.sh`?

1. **Memeriksa Prasyarat**: Memastikan Python 3.8+ dan mendeteksi ketersediaan Herdr.
2. **Auto-Config Herdr**: Jika Herdr sudah terpasang namun belum pernah dibuka, skrip akan membuat file `~/.config/herdr/config.toml` dengan `onboarding = false` agar tidak terhambat wizard awal.
3. **Global Store**: Menempatkan *system prompts* peran (PM, Analis/Tech Lead, Coder, Dokumenter), dokumen template, dan panduan ke `~/.gemini/team-orch/`.
4. **Symlink CLI**: Mendaftarkan `team-orch`, `herdr-orch`, dan `team-orch-uninstall` ke `~/.local/bin/`.
5. **Skill & Rules**: Mendaftarkan custom skill `team-orchestrator` ke `~/.gemini/config/skills/` dan aturan ketat (Read-Only Git, Model Auto-Switch) ke `~/.gemini/GEMINI.md`.

---

## 🗑️ 3. Cara Menghapus Framework Secara Utuh (Clean Uninstall)

Jika Anda atau rekan yang Anda bagikan framework ini ingin menghapusnya secara total dari komputer tanpa meninggalkan sampah konfigurasi:

Jalankan perintah ini dari terminal mana saja:
```bash
team-orch-uninstall
```
Atau langsung dari folder repositori:
```bash
./installer/uninstall.sh
```

### Apa yang dibersihkan oleh `uninstall.sh`?
- Menghapus symlink CLI (`team-orch`, `herdr-orch`, `team-orch-uninstall`) dari `~/.local/bin/`.
- Menghapus seluruh direktori data global `~/.gemini/team-orch/`.
- Menghapus pendaftaran skill `~/.gemini/config/skills/team-orchestrator/`.
- Mencadangkan dan menonaktifkan aturan `~/.gemini/GEMINI.md`.
- Komputer kembali bersih seperti semula.
