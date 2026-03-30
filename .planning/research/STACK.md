# Stack Research

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
