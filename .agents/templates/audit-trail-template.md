# Audit Trail & Activity Log: [PROJECT_NAME_OR_ID]

> **Kebijakan Transparansi & Akuntabilitas**:  
> Seluruh agen (PM, Analis, Coder, Dokumenter) **WAJIB** mencatat setiap tindakan teknis, eksekusi perintah, keputusan arsitektur, dan hasil review ke dalam log ini secara kronologis (*append-only*).  
> Seluruh anggota tim wajib memantau dan memverifikasi integritas log ini untuk mendeteksi anomali, performa lambat, deviasi teknis, atau potensi risiko keamanan.

---

## 1. Dashboard Ringkasan & Metrik Performa
- **ID Proyek**: `[PROJECT_NAME_OR_ID]`
- **Status Keamanan Global**: `CLEAN / SECURE`
- **Total Aksi Terekam**: 0
- **Terakhir Diperbarui**: `[YYYY-MM-DD HH:MM:SS]`

---

## 2. Catatan Kronologis Aktivitas (*Append-Only Log*)

### Format Entri Log:
<!-- 
### [AUDIT-XXX] YYYY-MM-DD HH:MM:SS | [ROLE] | [EVENT_NAME]
- **Pelaksana (Actor)**: [Nama Peran / Model yang Digunakan]
- **Tindakan / Proses**: [Deskripsi ringkas aktivitas yang dikerjakan]
- **File & Artefak**:
  - Dibuat / Dimodifikasi: `path/to/file`
- **Detail Teknis & Performa**:
  - Perintah Shell: `[command yang dijalankan jika ada]`
  - Durasi / Waktu Eksekusi: `[misal: 0.25s]`
  - Status Keluaran: `[Exit Code 0 / PASS]`
- **Validasi Keamanan (Security Audit Check)**:
  - Sanitasi Input: `[PASS | N/A]`
  - Git State Protection (Read-Only Git): `[PASS - No git mutating commands]`
  - Secrets & Credentials: `[PASS - No plain secrets exposed]`
  - Workspace Boundary: `[PASS - Changes strictly within workspace]`
- **Kesimpulan / Next Step**: [Apa langkah lanjutan yang dihasilkan]
-->
