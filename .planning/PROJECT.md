# Domain-Specific AI for Government Bond Risk Analysis

## What This Is

This project is a master's seminar deliverable implemented as a reproducible Python and Quarto pipeline. It predicts whether sovereign bond spreads versus the German Bund will widen or narrow next month for selected Eurozone countries by combining structured macro and market data with text sentiment from ECB communications and, if feasible, related financial text.

## Core Value

Produce a defensible end-to-end research pipeline that runs reliably and shows whether domain-specific structured plus NLP features can outperform structured-only baselines on next-month sovereign spread direction.

## Requirements

### Validated

- ✓ ECB monthly 10Y bond yield collection for DE, FR, IT, ES, PT, GR works from code in `src/data_collection/collect_bond_yields.py`
- ✓ Monthly HICP and unemployment collection and merge pipeline works from code in `src/data_collection/collect_macro_data.py`

### Active

- [ ] Build the final country-month modeling dataset with target variable, lags, and quality checks
- [ ] Add an NLP sentiment layer that can be merged cleanly at monthly frequency
- [ ] Train and compare baseline ML and main deep learning models using time-based splits
- [ ] Prepare a Quarto report that runs end-to-end and documents methods, results, and interpretation
- [ ] Run a manual LLM benchmark on 30 held-out test cases

### Out of Scope

- Full production app or dashboard — the professor requires a working notebook/script pipeline, not an application
- High-frequency daily modeling as the primary dataset grain — macro variables are monthly or quarterly and would be misaligned
- Broad multi-asset or global fixed-income coverage — this would dilute the seminar scope and increase data complexity
- Paid data vendors or proprietary news feeds — the project is constrained to free or publicly accessible sources

## Context

- Repository already contains working data collection scripts and processed CSV outputs from Session 1.
- Current country scope is DE as benchmark plus FR, IT, ES, PT, and GR as modeled countries.
- Frequency choice is monthly, which matches the macro series and keeps the problem academically defensible.
- The target framing is binary classification on next-month spread direction.
- The expected deliverable is a single `.qmd` file plus supporting Python modules that execute end-to-end.
- The strongest differentiation is likely to come from careful feature construction, monthly text aggregation, and transparent comparison against structured-only baselines rather than from model complexity alone.
- Text sentiment may or may not improve performance; a null result is still academically valid if measured cleanly.

## Constraints

- **Deliverable**: End-to-end Python and Quarto pipeline — seminar assessment favors reproducibility over productization
- **Timeline**: Short academic project timeline — favors incremental phases and early baseline results
- **Data Availability**: Free public sources only — feature set must align to ECB, Eurostat, ECB statements, and similar open materials
- **Frequency**: Monthly dataset grain — chosen to align macro, yields, and text aggregation cleanly
- **Evaluation**: Time-based validation only — random shuffling would create leakage for this forecasting task
- **Environment**: Python 3.13 in local virtual environment — implementation should stay lightweight and reproducible

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Use monthly frequency | Aligns macro data and avoids noisy, weakly justified repetition of slower-moving indicators | ✓ Good |
| Use Eurozone sovereign spreads vs Germany | Keeps monetary regime consistent while preserving credit-risk variation | ✓ Good |
| Deliver a Quarto report instead of an app | Matches course expectations and reduces non-core engineering work | ✓ Good |
| Treat text sentiment as additive evidence, not guaranteed uplift | Prevents overclaiming and keeps the project valid if NLP adds little | ✓ Good |
| Start with structured baselines before FinBERT integration | Baselines are necessary to judge whether the text layer adds value | ✓ Good |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** via `$gsd-transition`:
1. Requirements invalidated? Move to Out of Scope with reason.
2. Requirements validated? Move to Validated with phase reference.
3. New requirements emerged? Add to Active.
4. Decisions to log? Add to Key Decisions.
5. "What This Is" still accurate? Update if drifted.

**After each milestone** via `$gsd-complete-milestone`:
1. Full review of all sections.
2. Core Value check.
3. Audit Out of Scope reasons.
4. Update Context with current state.

---
*Last updated: 2026-03-29 after initialization*
