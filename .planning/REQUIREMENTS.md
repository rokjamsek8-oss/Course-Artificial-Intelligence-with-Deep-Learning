# Requirements: Domain-Specific AI for Government Bond Risk Analysis

**Defined:** 2026-03-29
**Core Value:** Produce a defensible end-to-end research pipeline that runs reliably and shows whether domain-specific structured plus NLP features can outperform structured-only baselines on next-month sovereign spread direction.

## v1 Requirements

### Data Pipeline

- [ ] **DATA-01**: User can collect monthly 10Y sovereign yields for DE, FR, IT, ES, PT, and GR from public sources
- [ ] **DATA-02**: User can collect monthly macro indicators and merge them with yield-derived features at country-month grain
- [ ] **DATA-03**: User can build a final modeling dataset with next-month spread-direction target and lagged predictors
- [ ] **DATA-04**: User can run dataset quality checks that report date coverage, missingness, and class balance

### NLP Features

- [ ] **NLP-01**: User can score ECB or related financial text with FinBERT sentiment
- [ ] **NLP-02**: User can aggregate text scores to monthly features that merge with the modeling dataset
- [ ] **NLP-03**: User can document the text source, aggregation rule, and limitations in the report

### Modeling

- [ ] **MOD-01**: User can train a logistic regression baseline on structured features only
- [ ] **MOD-02**: User can train a random forest baseline on structured features only
- [ ] **MOD-03**: User can train a PyTorch MLP using structured and text-derived features
- [ ] **MOD-04**: User can evaluate all models with time-based train/test splits and report accuracy, F1, and ROC-AUC

### Comparison And Reporting

- [ ] **EVAL-01**: User can generate a fixed sample of 30 held-out test cases for manual LLM benchmarking
- [ ] **EVAL-02**: User can compare baseline, main model, and manual LLM predictions in a consistent scoring table
- [ ] **REP-01**: User can render a Quarto report that runs end-to-end and includes data, methods, results, and conclusion
- [ ] **REP-02**: User can show whether text sentiment improved performance, had no effect, or worsened performance without overstating the result

## v2 Requirements

### Extended Data

- **DATA-05**: User can add additional macro variables such as GDP growth, debt-to-GDP, or fiscal metrics if joins are defensible
- **DATA-06**: User can add country-specific news sentiment beyond ECB communications

### Modeling Extensions

- **MOD-05**: User can test sequential models such as LSTM after the MLP baseline is stable
- **MOD-06**: User can add explainability outputs such as feature importance or SHAP-style diagnostics

## Out of Scope

| Feature | Reason |
|---------|--------|
| Production web app | Not required for the seminar deliverable |
| Real-time prediction service | Adds infrastructure work without helping the research question |
| Daily-frequency master dataset | Misaligned with macro publication frequency and increases leakage risk |
| Broad global bond universe | Expands scope beyond what the current project can validate well |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| DATA-01 | Phase 1 | In Progress |
| DATA-02 | Phase 1 | In Progress |
| DATA-03 | Phase 2 | Pending |
| DATA-04 | Phase 2 | Pending |
| NLP-01 | Phase 3 | Pending |
| NLP-02 | Phase 3 | Pending |
| NLP-03 | Phase 5 | Pending |
| MOD-01 | Phase 2 | Pending |
| MOD-02 | Phase 2 | Pending |
| MOD-03 | Phase 4 | Pending |
| MOD-04 | Phase 4 | Pending |
| EVAL-01 | Phase 5 | Pending |
| EVAL-02 | Phase 5 | Pending |
| REP-01 | Phase 5 | Pending |
| REP-02 | Phase 5 | Pending |

**Coverage:**
- v1 requirements: 15 total
- Mapped to phases: 15
- Unmapped: 0 ✓

---
*Requirements defined: 2026-03-29*
*Last updated: 2026-03-29 after initial definition*
