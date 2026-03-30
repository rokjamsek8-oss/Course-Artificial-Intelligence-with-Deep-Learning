---
phase: 1
slug: data-foundation
status: draft
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-29
---

# Phase 1 - Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | other - command-driven script validation |
| **Config file** | none - direct Python script execution |
| **Quick run command** | `.\.venv\Scripts\python.exe -m py_compile src/data_collection/collect_bond_yields.py src/data_collection/collect_macro_data.py src/data_collection/build_phase1_panel.py` |
| **Full suite command** | `.\.venv\Scripts\python.exe src/data_collection/collect_bond_yields.py` then `.\.venv\Scripts\python.exe src/data_collection/collect_macro_data.py` then `.\.venv\Scripts\python.exe src/data_collection/build_phase1_panel.py` |
| **Estimated runtime** | ~15 seconds for smoke checks, ~60 seconds for full wave verification |

---

## Sampling Rate

- **After every task commit:** Run `.\.venv\Scripts\python.exe -m py_compile` for the Python files touched in that task
- **After every plan wave:** Run the full suite commands in sequence
- **Before `$gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 15 seconds for per-task smoke checks

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 1-01-01 | 01 | 1 | DATA-01 | syntax plus execution | `.\.venv\Scripts\python.exe -m py_compile src/data_collection/collect_bond_yields.py` then `.\.venv\Scripts\python.exe src/data_collection/collect_bond_yields.py` | Yes | pending |
| 1-01-02 | 01 | 1 | DATA-02 | syntax plus execution | `.\.venv\Scripts\python.exe -m py_compile src/data_collection/collect_macro_data.py` then `.\.venv\Scripts\python.exe src/data_collection/collect_macro_data.py` | Yes | pending |
| 1-02-01 | 02 | 2 | DATA-02 | execution | `.\.venv\Scripts\python.exe src/data_collection/build_phase1_panel.py` | Created by plan | pending |
| 1-02-02 | 02 | 2 | DATA-02 | file check | `Get-Content .planning\phases\01-data-foundation\01-data-contract.md` | Created by plan | pending |

*Status: pending, green, red, flaky*

---

## Wave 0 Requirements

Existing infrastructure covers this phase. No separate Wave 0 artifacts are required before execution.

---

## Manual-Only Verifications

All Phase 1 behaviors have automated verification.

---

## Validation Sign-Off

- [x] All tasks have automated verify or same-task artifact checks
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] No false Wave 0 dependencies remain
- [x] No watch-mode flags
- [x] Feedback latency < 15s for smoke checks
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
