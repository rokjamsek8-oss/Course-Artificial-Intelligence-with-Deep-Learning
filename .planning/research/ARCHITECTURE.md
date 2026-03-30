# Architecture Research

## Components

1. Data collection
   - Download sovereign yield data
   - Download macro series
   - Persist raw or processed tabular outputs
2. Dataset building
   - Align all sources at country-month grain
   - Create target and lagged features
   - Run quality checks and export final dataset
3. Text processing
   - Collect or curate ECB statement excerpts and related text
   - Score text with FinBERT
   - Aggregate sentiment features to mergeable monthly outputs
4. Modeling
   - Train structured-only baselines
   - Train combined structured-plus-text MLP
   - Save metrics, plots, and predictions
5. Evaluation and reporting
   - Generate comparison tables
   - Build LLM benchmark prompts and scoring template
   - Render Quarto report

## Data Flow

`APIs / documents -> processed CSVs -> final modeling table -> model outputs -> Quarto report`

## Suggested Build Order

1. Final dataset builder
2. Baseline models
3. Text sentiment pipeline
4. Combined model
5. LLM comparison helper
6. Quarto integration

This order minimizes risk by proving the numerical pipeline before adding NLP complexity.
