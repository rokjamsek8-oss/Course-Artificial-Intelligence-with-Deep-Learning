# Pitfalls Research

## Major Risks

### Data leakage from time splitting

- Warning signs: random train/test split, future values used in lag construction, or scalers fit on all data
- Prevention: split by date first, fit preprocessors on train only, and create target/lag columns carefully
- Phase coverage: dataset building and baseline modeling

### Misaligned frequencies

- Warning signs: daily bond data repeated against monthly macro observations or inconsistent month-end definitions
- Prevention: keep the canonical grain at country-month and define one month timestamp convention
- Phase coverage: dataset building

### Weak or noisy text linkage

- Warning signs: text features merged without a defensible month mapping or country relevance rule
- Prevention: start with ECB monthly communication sentiment, document the aggregation rule, and keep features limited
- Phase coverage: sentiment pipeline

### Over-scoping the seminar

- Warning signs: adding dashboards, too many countries, too many models, or too many sources before the baseline works
- Prevention: protect the Quarto pipeline as the main success criterion and defer extras
- Phase coverage: all phases

### Inconclusive comparison claims

- Warning signs: claiming superiority over a general LLM without a fixed evaluation procedure
- Prevention: define the 30-case benchmark and score it consistently against the held-out set
- Phase coverage: evaluation and report
