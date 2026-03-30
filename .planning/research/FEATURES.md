# Feature Research

## Table Stakes

- Monthly sovereign spread versus Germany
- One-month spread change
- Rolling spread volatility
- HICP inflation
- Unemployment rate
- Time-based train/test split
- Accuracy, F1, and ROC-AUC reporting

## High-Value Additions

- Lagged versions of market and macro variables
- Text sentiment aggregated to country-month or month-level macro sentiment
- Event flags for ECB meetings or notable rating actions
- Per-country descriptive coverage checks and missing-data diagnostics

## Nice-to-Have but Deferrable

- GDP growth or debt-to-GDP if reliable monthly or sensible lagged quarterly joins are available
- Embedding-based text features beyond simple sentiment
- LSTM or sequence models after the baseline MLP is working

## Recommendation

The project should prioritize a strong, auditable structured dataset and only then add a limited number of text-derived features that are easy to explain in the report.
