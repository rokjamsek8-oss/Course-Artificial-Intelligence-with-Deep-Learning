# Roadmap: Domain-Specific AI for Government Bond Risk Analysis

**Created:** 2026-03-29
**Granularity:** Standard
**Execution:** Parallel where safe, sequential on the critical path

## Summary

| Phase | Name | Goal | Requirements |
|-------|------|------|--------------|
| 1 | Data Foundation | Stabilize collection outputs and confirm the canonical country-month research frame | DATA-01, DATA-02 |
| 2 | Modeling Dataset And Baselines | Build the supervised dataset and prove structured-only baselines end-to-end | DATA-03, DATA-04, MOD-01, MOD-02 |
| 3 | Text Sentiment Pipeline | Add defensible monthly NLP features from ECB or related public text | NLP-01, NLP-02 |
| 4 | Combined Model Evaluation | Train and evaluate the MLP on structured plus text features using the same time-safe protocol | MOD-03, MOD-04 |
| 5 | Benchmark And Quarto Delivery | Run the manual LLM benchmark and package all evidence into the final report | NLP-03, EVAL-01, EVAL-02, REP-01, REP-02 |

## Phase 1: Data Foundation

**Goal:** Lock the canonical dataset grain, verify the existing collection code, and make the processed inputs stable enough for downstream modeling.

**Requirements:** DATA-01, DATA-02

**Success criteria:**
1. Bond and macro collection scripts run successfully from the repo without manual patching.
2. Processed CSVs have documented date ranges, country coverage, and known missingness.
3. A clear canonical join key and monthly timestamp convention is established for downstream modeling.
4. Any current collection issues are captured before feature engineering starts.

## Phase 2: Modeling Dataset And Baselines

**Goal:** Convert collected data into a supervised learning table and establish the structured-only benchmark.

**Requirements:** DATA-03, DATA-04, MOD-01, MOD-02

**Success criteria:**
1. Final dataset includes target variable, lagged predictors, and a reproducible split boundary.
2. Dataset quality checks print class balance, missingness summary, and feature inventory.
3. Logistic regression and random forest baselines both run on the held-out period.
4. Metrics are saved in a structured format for later comparison in the report.

## Phase 3: Text Sentiment Pipeline

**Goal:** Build a minimal, defensible NLP feature layer that can be merged into the monthly dataset.

**Requirements:** NLP-01, NLP-02

**Success criteria:**
1. A reproducible text input source is selected and documented.
2. FinBERT sentiment extraction runs locally on sample or collected text.
3. Sentiment outputs are aggregated into monthly features with a documented merge rule.
4. The resulting feature file joins cleanly to the modeling dataset.

## Phase 4: Combined Model Evaluation

**Goal:** Measure whether adding text-derived features improves the forecasting pipeline relative to structured-only baselines.

**Requirements:** MOD-03, MOD-04

**Success criteria:**
1. The MLP training script runs end-to-end on the combined dataset.
2. Evaluation uses the same held-out split and metrics as the baselines.
3. Results clearly compare structured-only and structured-plus-text performance.
4. The project can state whether the text layer helped, hurt, or had negligible effect.

## Phase 5: Benchmark And Quarto Delivery

**Goal:** Turn the experiments into a submission-ready artifact with a disciplined manual LLM comparison.

**Requirements:** NLP-03, EVAL-01, EVAL-02, REP-01, REP-02

**Success criteria:**
1. A fixed 30-case benchmark set and scoring template are generated from the held-out period.
2. The comparison table can accommodate baseline, MLP, and manually collected LLM predictions.
3. The Quarto document executes from data load through final charts and tables.
4. The final report states limitations, methodology, and findings without overclaiming.

## Critical Path

Phase 1 -> Phase 2 -> Phase 3 -> Phase 4 -> Phase 5

Some work inside Phases 3 and 5 can run in parallel, but the modeling critical path depends on a stable Phase 2 dataset first.

---
*Last updated: 2026-03-29 after roadmap creation*
