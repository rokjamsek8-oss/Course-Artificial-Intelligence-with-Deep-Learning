# Research Summary

## Stack

Stay with the current Python stack: pandas, scikit-learn, PyTorch, transformers, and Quarto. This is enough to support a disciplined academic pipeline without adding engineering overhead.

## Table Stakes

- Clean country-month modeling table
- Time-safe baseline models
- Transparent evaluation metrics
- Executable Quarto report

## Differentiators Worth Pursuing

- FinBERT-based monthly sentiment features
- Clear explanation of whether text adds incremental predictive value
- Manual LLM benchmark on a fixed held-out sample

## Watch Out For

- Leakage and misaligned time joins
- Overly ambitious text sourcing before the baseline pipeline is stable
- Claims about beating LLMs without a stable scoring protocol

## Planning Guidance

The next roadmap should push the repo from data collection to a fully reproducible modeling and reporting pipeline. The critical path is:

1. Build the final dataset and baseline models
2. Add text sentiment and merge it
3. Train and compare the combined model
4. Package the evidence into Quarto
