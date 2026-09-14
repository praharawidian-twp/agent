# Sub-Task Implementation Checklist: [PROJECT_NAME_OR_ID]

> Disusun oleh: **Analis**  
> Dikerjakan oleh: **Coder**  
> Direview oleh: **Analis**  
> Terakhir Diperbarui: `[YYYY-MM-DD]`

---

## Ringkasan Progres

- Total Sub-Task: `[N]`
- Selesai (`DONE`): `0`
- Sedang Dikerjakan: `TASK-01`

---

## Daftar Sub-Task

### [ ] TASK-01: [Judul Sub-Task Pertama]
- **Target File**:
  - Implementasi: `path/to/source_file.py`
  - Unit Test: `tests/test_source_file.py`
- **Instruksi Spesifik**:
  - [Jelaskan apa yang harus dibuat atau diubah pada file sumber]
- **Kebutuhan Unit Test (Wajib)**:
  - [ ] Test fungsi normal (*happy path*)
  - [ ] Test penanganan error / edge case
- **Perintah Verifikasi Test**:
  ```bash
  pytest tests/test_source_file.py
  ```
- **Status Review**: `[PENDING | NEEDS_REVISION | APPROVED]`

---

### [ ] TASK-02: [Judul Sub-Task Kedua]
- **Target File**:
  - Implementasi: `path/to/another_file.py`
  - Unit Test: `tests/test_another_file.py`
- **Instruksi Spesifik**:
  - [Jelaskan detail implementasi]
- **Kebutuhan Unit Test (Wajib)**:
  - [ ] Test integrasi atau skenario terkait
- **Perintah Verifikasi Test**:
  ```bash
  pytest tests/test_another_file.py
  ```
- **Status Review**: `[PENDING | NEEDS_REVISION | APPROVED]`

---

## Aturan Transisi Status
1. Coder hanya boleh mencentang task jika Analis sudah mencatat **APPROVED** di `review-log.md`.
2. Format tanda selesai: Ubah `### [ ] TASK-XX:` menjadi `### [x] TASK-XX: ... (DONE)`.
