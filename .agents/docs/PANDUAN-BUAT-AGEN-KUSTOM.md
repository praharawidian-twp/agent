# Panduan Lengkap: Cara Membuat Agen Spesifik Kustom (Custom Agents)

Dokumen ini adalah panduan standar untuk membuat agen otonom baru di luar alur kerja bawaan (PM ➔ Analis ➔ Coder ➔ Dokumenter).  
Anda bisa membaca panduan ini atau **cukup memberikan file ini ke AI** dan meminta AI membuatkan agen baru untuk Anda!

---

## 1. Tiga Metode Membuat Agen Baru

| Metode | Tempat Penyimpanan | Kapan Digunakan? | Konsumsi Token |
| :--- | :--- | :--- | :--- |
| **A. Global Skill (Direkomendasikan)** | `~/.gemini/config/skills/<nama>/SKILL.md` | Prosedur kerja mandiri, runbook spesialis (DevOps, Data Analyst, Security Auditor) yang berlaku di semua proyek & IDE. | **Paling Hemat** (Progressive disclosure, hanya dipanggil saat dibutuhkan). |
| **B. Role File Team-Orch** | `~/.gemini/team-orch/roles/<nama>.md` | Agen yang ingin diintegrasikan ke sistem tim `team-orch` dan bisa didelegasikan ke worker pane Herdr. | **Hemat** (Dipanggil via `team-orch dispatch`). |
| **C. Dynamic Subagent (Ad-Hoc)** | Sementara di sesi memori | Tugas sekali-jalan saat itu juga (misal: "Optimasi 1 file SQL ini"). | **Sedang** (Dibuat dan dibubarkan on-the-fly). |

---

## 2. Template Metode A: Membuat Global Skill Baru

Buat folder baru: `~/.gemini/config/skills/<nama-agen>/` dan file `SKILL.md`:

```markdown
---
name: [nama-agen-kebab-case]
description: [Deskripsi peran orang ketiga: apa fungsinya dan KAPAN sistem harus memanggilnya]. Contoh: "Gunakan skill ini ketika pengguna meminta audit keamanan, scanning celah OWASP, atau memeriksa kerentanan dependensi."
---

# [Nama Agen / Judul Spesialis]

## 1. Identitas & Tanggung Jawab
Anda bertindak sebagai [Peran Spesialis].
Tugas utama Anda adalah [deskripsi tugas spesifik].

- Rekomendasi Model: `gemini-3.8-flash-high` (kecepatan & akurasi) atau `gemini-3.1-pro-high` (analisis mendalam).
- Lingkup Kerja: [Fokus area kerja].

## 2. Prinsip Kerja & Batasan (Do's & Don'ts)
- WAJIB: [Hal wajib, misal: selalu sertakan bukti log eksekusi].
- DILARANG: [Batasan ketat, misal: dilarang mengubah konfigurasi produksi].

## 3. Alur Kerja Langkah Demi Langkah (Step-by-Step Runbook)
1. Langkah 1: [Analisis input]
2. Langkah 2: [Eksekusi alat/skrip]
3. Langkah 3: [Sajikan laporan ringkas dan terukur]
```

---

## 3. Template Metode B: Membuat Role Baru di Team-Orch

Buat file baru di `~/.gemini/team-orch/roles/<nama-role>.md`:

```markdown
# Role: [Nama Peran] ([Spesialisasi])

## 1. Identitas & Tanggung Jawab Utama
Anda bertindak sebagai **[Nama Peran]** dalam tim.
Tugas utama Anda: [Deskripsi].

- **Tingkat Kompleksitas**: [Rendah / Sedang / Tinggi]
- **Rekomendasi Model**: `gemini-3.8-flash-high` / `gemini-3.1-pro-high`
- **Output Utama**: [File hasil kerja]

---

## 2. Prinsip Kerja & Batasan
1. [Prinsip 1]
2. [Prinsip 2]
3. **No Git Modification**: Dilarang menjalankan `git add`, `git commit`, `git push`.
4. **Audit Trail**: Catat setiap tindakan penting ke `audit-trail.md`.

---

## 3. Alur Kerja Standar (Workflow)
1. Baca input atau task terkait.
2. Jalankan eksekusi teknis.
3. Catat log hasil kerja ke audit trail.
```

---

## 4. Cara Praktis: Menyuruh AI Membuatkan Agen untuk Anda

Anda tidak perlu menulis kode sendiri. Cukup copy-paste perintah ini ke obrolan AI di Control Room:

> *"Tolong buatkan agen spesifik baru untuk **[sebutkan kebutuhan, contoh: DevOps SRE untuk Docker & Kubernetes]** menggunakan standar Metode A pada `docs/PANDUAN-BUAT-AGEN-KUSTOM.md`. Simpan skill tersebut di `~/.gemini/config/skills/devops-sre/SKILL.md`."*

AI akan langsung menyusun frontmatter YAML, batasan, rekomendasi model, dan alur kerja sesuai standar sistem kita!
