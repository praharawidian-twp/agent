# Multi-Agent Coordination & Herdr Rules

- Workspace: Herdr multi-pane orchestration enabled.
- Primary role: Main session acts as Orchestrator.
- Subtask delegation: Always check target pane rate limits with `herdr-orch check-limit <pane_id>` prior to task delegation.
- Model auto-switch:
  - Low complexity -> `gemini-3.8-flash-low`
  - Medium complexity -> `gemini-3.8-flash-high`
  - High complexity -> `gemini-3.1-pro-high`
- Utility: `herdr-orch` CLI installed at `/Users/macbook/.local/bin/herdr-orch`.
- Git Policy (CRITICAL):
  - Agents are strictly FORBIDDEN from modifying Git state (`git add`, `git commit`, `git push`, `git merge`, etc.).
  - Only read-only inspections (`git status`, `git diff`, `git log`) are permitted.
- Analyst Evaluation Standard (Senior Lead Engineer / Tech Lead):
  - The Analyst acts as a **Senior Lead Developer / Tech Lead**, not just a passive reviewer.
  - The Analyst **MUST** read, understand, and enforce the project's existing boilerplate, architecture conventions, idioms, and technical standards.
  - The Analyst must **NOT** solely focus on passing unit tests.
  - The Analyst **MUST** thoroughly safeguard all technical aspects: clean code, security best practices, maintainability, edge cases, reusable utilities, and strict alignment with user requirements (`01-requirements.md`).
- Autonomous Multi-Agent Fleet Topology & Monitoring Room:
  - 1 Role = 1 Dedicated Pane: Setiap peran memiliki pane tersendiri (PM di Control Room pane, Analis di pane terpisah, Coder di pane terpisah, dll).
  - Control Room Siaga: Pane utama/PM (w1:p4) KHUSUS untuk komunikasi interaktif langsung dengan Pengguna dan monitoring tim. Dilarang menjalankan proses eksekusi kode atau blocking task di pane Control Room agar pengguna selalu dapat berdialog setiap saat.
  - Otomatis Masuk ke agy-auto: Setiap pane worker agen baru secara otomatis meluncurkan sesi `agy-auto` sesuai tier modelnya (Analis: gemini-3.1-pro-high, Coder: gemini-3.8-flash-high, Dokumenter: gemini-3.8-flash-low).
  - Validasi agy-auto: Sistem wajib memeriksa ketersediaan binary `agy-auto` di PATH. Jika belum ada, sistem wajib meminta persetujuan pengguna untuk memasang wrapper `agy-auto` (`exec agy --dangerously-skip-permissions "$@"`), dan jika disetujui langsung mengeksekusi pemasangan.
  - Perkenalan Diri Wajib (Role Self-Introduction): Setiap kali agen aktif di suatu pane, agen wajib memperkenalkan perannya secara eksplisit di awal percakapan (`Halo Pengguna & Tim! Saya [Role]...`).
  - Komunikasi Antar-Agen Real-Time: Coder dan Analis saling berbalas prompt secara transparan antar-pane (misal: Coder mengajukan Review Request ke pane Analis, dan Analis membalas dengan Code Review & status Approval) sehingga pengguna dapat melihat dinamika kolaborasi secara langsung di layar Herdr.
  - Penyelarasan Ekspektasi Status: Sebelum menonaktifkan, mengubah, atau mematikan sesi agy-auto di pane manapun, PM wajib memberitahukan pengguna terlebih dahulu.



