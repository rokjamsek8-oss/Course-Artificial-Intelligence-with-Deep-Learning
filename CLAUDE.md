# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Master's seminar project: **Domain-Specific AI for Government Bond Risk Analysis**. Binary classification predicting whether sovereign bond spreads (vs German Bund) will widen (1) or narrow (0) next month.

- **Countries**: DE (benchmark), FR, IT, ES, PT, GR
- **Period**: 2019–2025, monthly frequency
- **Deliverable**: Single Quarto Markdown (`.qmd`) file that runs end-to-end

## Architecture

1. **Data collection** — ECB Statistical Data Warehouse API (no key needed)
2. **Text sentiment** — FinBERT on ECB statements and financial news
3. **Baseline models** — Logistic regression, random forest (structured data only)
4. **Main model** — MLP neural network (structured + text features, PyTorch)
5. **LLM baseline** — Comparison on 30 test cases
6. **Evaluation** — Accuracy, F1, ROC-AUC

## Data APIs

- **Bond yields (ECB)**: `IRS/M.{CC}.L.L40.CI.0000.EUR.N.Z?format=csvdata` — country codes: DE, FR, IT, ES, PT, GR
- **HICP inflation (ECB)**: `ICP/M.{CC}.N.000000.4.ANR?format=csvdata`
- **Unemployment (Eurostat)**: `une_rt_m/M.SA.TOTAL.PC_ACT.T.{GEO}?format=SDMX-CSV` — uses EL for Greece (not GR)

Base URLs:
- ECB: `https://data-api.ecb.europa.eu/service/data/`
- Eurostat: `https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/`

## Environment

- **Python**: 3.13 (virtual environment in `.venv/`)
- **Activate venv**: `.venv/Scripts/activate` (Windows) or `source .venv/bin/activate` (Unix)
- **Key libraries**: pandas, scikit-learn, PyTorch, transformers (FinBERT), matplotlib

## Progress

### Session 1 (2026-03-28)
- Bond yield collection complete: `src/data_collection/collect_bond_yields.py`
  - All 6 countries, 86 months (2019-01 to 2026-02), no missing values
  - Computes spread vs DE, 1-month change, 3-month rolling volatility
  - Output: `data/processed/bond_yields.csv` (430 rows)
- Macro data collection complete: `src/data_collection/collect_macro_data.py`
  - HICP inflation from ECB, unemployment from Eurostat
  - Merged with bond yield data
  - Output: `data/processed/macro_features.csv` (515 rows)
- ECB rate-limits aggressively — use 1s+ delay between requests
- Eurostat uses `EL` for Greece; ECB uses `GR` — mapping handled in code
- **Next**: text sentiment extraction (FinBERT), target variable creation, baseline models

<!-- GSD:project-start source:PROJECT.md -->
## Project

**Domain-Specific AI for Government Bond Risk Analysis**

This project is a master's seminar deliverable implemented as a reproducible Python and Quarto pipeline. It predicts whether sovereign bond spreads versus the German Bund will widen or narrow next month for selected Eurozone countries by combining structured macro and market data with text sentiment from ECB communications and, if feasible, related financial text.

**Core Value:** Produce a defensible end-to-end research pipeline that runs reliably and shows whether domain-specific structured plus NLP features can outperform structured-only baselines on next-month sovereign spread direction.

### Constraints

- **Deliverable**: End-to-end Python and Quarto pipeline — seminar assessment favors reproducibility over productization
- **Timeline**: Short academic project timeline — favors incremental phases and early baseline results
- **Data Availability**: Free public sources only — feature set must align to ECB, Eurostat, ECB statements, and similar open materials
- **Frequency**: Monthly dataset grain — chosen to align macro, yields, and text aggregation cleanly
- **Evaluation**: Time-based validation only — random shuffling would create leakage for this forecasting task
- **Environment**: Python 3.13 in local virtual environment — implementation should stay lightweight and reproducible
<!-- GSD:project-end -->

<!-- GSD:stack-start source:research/STACK.md -->
## Technology Stack

## Recommended Stack
- Python for all collection, preprocessing, modeling, and report execution
- Pandas for country-month dataset construction
- Scikit-learn for logistic regression, random forest, preprocessing, and metrics
- PyTorch for the MLP model
- Hugging Face `transformers` for FinBERT sentiment inference
- Quarto for the final executable report
- Matplotlib or Seaborn for figures embedded in the report
## Why This Stack Fits
- It matches the current repo and the deliverable already chosen.
- It is lightweight enough for a seminar project while still covering classical ML and deep learning.
- It preserves a clean comparison between baselines and the neural model.
## Implementation Notes
- Keep reusable code in `src/` and orchestrate execution from the Quarto file.
- Avoid adding infrastructure or app frameworks.
- Prefer deterministic preprocessing and explicit saved outputs under `data/processed/` and `results/`.
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

Conventions not yet established. Will populate as patterns emerge during development.
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->
## Architecture

Architecture not yet mapped. Follow existing patterns found in the codebase.
<!-- GSD:architecture-end -->

<!-- GSD:workflow-start source:GSD defaults -->
## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd:quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd:debug` for investigation and bug fixing
- `/gsd:execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->

<!-- GSD:profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd:profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
