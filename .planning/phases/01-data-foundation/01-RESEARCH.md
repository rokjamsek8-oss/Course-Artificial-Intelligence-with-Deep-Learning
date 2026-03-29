# Phase 1: Data Foundation - Research

**Researched:** 2026-03-29
**Domain:** Monthly sovereign-yield and macroeconomic data pipeline stabilization
**Confidence:** HIGH

## User Constraints

No `CONTEXT.md` exists for this phase.

Planning constraints must therefore come from:
- `.planning/ROADMAP.md` Phase 1 scope and success criteria
- `.planning/REQUIREMENTS.md` requirements `DATA-01` and `DATA-02`
- `CLAUDE.md` project constraints and environment guidance

## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| DATA-01 | User can collect monthly 10Y sovereign yields for DE, FR, IT, ES, PT, and GR from public sources | Verified current collector runs live against ECB and writes a 5-country spread panel with 86 months per modeled country |
| DATA-02 | User can collect monthly macro indicators and merge them with yield-derived features at country-month grain | Verified current macro collector runs live, but current merge shape is not yet canonical for modeling because it outer-joins DE-only rows and retains partial trailing months |

## Summary

The current repo already has working Phase 1 collection code and checked-in processed outputs. Both collectors executed successfully against the live ECB and Eurostat APIs on 2026-03-29 when run outside the sandbox. That materially changes planning: this phase is not about inventing a new collection stack, it is about locking the canonical panel definition, making the merge semantics explicit, and adding repeatable validation so downstream modeling does not inherit ambiguous rows.

The main structural issue is in the processed macro file, not the raw collection logic. `bond_yields.csv` is already close to the right modeling grain: one row per modeled country-month for `FR`, `IT`, `ES`, `PT`, `GR`, with German yields carried as benchmark columns. `macro_features.csv` is currently an outer merge that adds 85 Germany-only rows with no bond features and extends non-DE countries into partially observed months. That is acceptable as an intermediate diagnostic artifact, but it should not be treated as the canonical modeling input.

The stable planning assumption for this repo is: lock the canonical downstream grain to non-DE `country` x `month_start`, preserve DE only as benchmark feature columns, and define a complete-case usable window ending at `2025-12`. The trailing `2026-01` and `2026-02` rows should remain visible in collection outputs for freshness checks, but Phase 1 should produce a second, explicitly validated stabilized dataset or manifest that marks `2025-12` as the last fully populated month across all modeled countries.

**Primary recommendation:** Build Phase 1 around formalizing a single non-DE country-month panel with month-start timestamps, a `2025-12` completeness cutoff, and fixture-backed collector validation before any feature engineering begins.

## Project Constraints (from CLAUDE.md)

- Deliverable remains a reproducible Python plus Quarto pipeline, not an app.
- Country scope is fixed to `DE` benchmark plus `FR`, `IT`, `ES`, `PT`, `GR`.
- Core research period is monthly frequency over roughly `2019-2025`; daily master-data expansion is out of scope.
- Data sources must stay free and public.
- Evaluation later must use time-based validation only.
- Environment target is Python `3.13` in local `.venv/`.
- Reusable pipeline code should stay in `src/`.
- Prefer deterministic preprocessing and explicit saved outputs under `data/processed/` and `results/`.
- Avoid adding infrastructure or app frameworks.
- Phase work should stay inside the GSD workflow, not ad hoc repo edits.

## Standard Stack

### Core

| Library / Tool | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python | 3.13.12 | Runtime for collection and preprocessing | Matches repo environment and seminar pipeline scope |
| pandas | 3.0.1 | CSV ingest, month alignment, joins, quality summaries | Already in use; sufficient for this panel-building phase |
| requests | 2.33.0 | HTTP fetches from ECB and Eurostat APIs | Already in use; lightweight and appropriate |
| ECB Data Portal API | live web service | Sovereign yields and HICP source | Official public source; repo already uses current `data-api.ecb.europa.eu` base |
| Eurostat SDMX 2.1 API | live web service | Unemployment source | Official public source with stable SDMX 2.1 contract |

### Supporting

| Library / Tool | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| pytest | not installed | Local regression tests with recorded API fixtures | Add in Wave 0 for stable collector verification |
| Quarto | 1.9.36 | Later reporting and optional data appendix smoke checks | Not required for Phase 1 execution, but already available |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Outer-joining bond and macro tables | Left-join macro onto the non-DE bond panel | Left join is the correct canonical modeling shape here; outer join is only useful for diagnostics |
| Keeping live-only validation | Recorded fixture tests plus optional live smoke run | Fixture tests are faster and stable; live smoke remains useful but should not be the only check |
| Carrying DE as a row in the panel | Carry DE only as explicit benchmark columns | Separate DE rows break the modeling grain and create misleading missingness |

**Installation:**
```bash
.\.venv\Scripts\python.exe -m pip install pytest
```

**Version verification:**
- Verified from the local project environment on 2026-03-29:
  - Python `3.13.12`
  - pandas `3.0.1`
  - requests `2.33.0`
  - Quarto `1.9.36`

## Architecture Patterns

### Recommended Project Structure

```text
src/
+-- data_collection/          # Live collectors per source family
+-- data_processing/          # Canonical panel build + validation reports
+-- data_validation/          # Dataset assertions or summary checks

data/
+-- raw/                      # Optional cached raw API responses or fixture exports
+-- processed/                # Saved CSV outputs used by later phases

tests/
+-- data_collection/          # Fixture-backed collector tests
```

### Pattern 1: Canonical Non-DE Panel
**What:** Treat the downstream modeling panel as one row per modeled country-month for `FR`, `IT`, `ES`, `PT`, `GR`.

**When to use:** For every processed file intended to feed feature engineering, target construction, or modeling.

**Example:**
```python
# Source: repo evidence + ECB API contract
bonds = pd.read_csv("data/processed/bond_yields.csv", parse_dates=["date"])
macro = pd.read_csv("data/processed/macro_features.csv", parse_dates=["date"])

panel = bonds.merge(
    macro[["date", "country", "hicp_inflation", "unemployment_rate"]],
    on=["date", "country"],
    how="left",
    validate="one_to_one",
)
```

### Pattern 2: Month-Start Timestamp Contract
**What:** Normalize timestamps to the first day of each month and use that exact value as the join key.

**When to use:** Immediately after every API fetch and before every join or coverage assertion.

**Example:**
```python
# Source: https://data.ecb.europa.eu/help/api/data
df["date"] = pd.to_datetime(df["date"]).dt.to_period("M").dt.to_timestamp()
```

### Pattern 3: Freshness Window Separate from Stable Window
**What:** Preserve the freshest collected months in raw/intermediate outputs, but compute a separate stable cutoff for downstream use.

**When to use:** Whenever one source updates faster than another, which is already true here.

**Example:**
```python
feature_cols = [
    "yield", "yield_de", "spread", "spread_change_1m",
    "spread_vol_3m", "hicp_inflation", "unemployment_rate",
]

panel["is_complete"] = panel[feature_cols].notna().all(axis=1)
stable_end = (
    panel.groupby("date")["is_complete"]
    .all()
    .pipe(lambda s: s[s].index.max())
)
```

### Anti-Patterns to Avoid

- **Treating `macro_features.csv` as the canonical model table:** It currently contains DE-only rows and trailing partial months.
- **Using an outer join for downstream modeling inputs:** That shape hides grain violations instead of preventing them.
- **Encoding completeness by manual inspection:** Phase 1 should write explicit assertions or a machine-readable coverage summary.
- **Assuming latest months are fully populated because the yield collector succeeded:** They are not; the current complete non-DE window ends at `2025-12`.
- **Relying only on live API runs for verification:** Sandbox and network conditions can fail independently of code correctness.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| HTTP client abstraction | Custom API wrapper framework | `requests` with clear series URLs and parameters | The collectors are small and the APIs are simple |
| Month alignment logic | String slicing and manual month parsing | `pandas.to_datetime(...).dt.to_period("M").dt.to_timestamp()` | Avoids silent join drift |
| Country-code inference | Heuristic country renaming | Explicit `ECB_TO_EUROSTAT` mapping | Greece already proves the codes differ (`GR` vs `EL`) |
| Data-quality review | Spreadsheet-only checking | Scripted assertions and printed coverage tables | Prevents regressions and supports reproducibility |
| Live API regression tests | Full end-to-end network dependence in CI | Recorded fixture tests plus optional manual smoke run | Stable and fast, while still preserving one real-world verification path |

**Key insight:** Phase 1 risk is not missing technical complexity; it is accidental ambiguity. Simple, explicit pandas-based contracts are better than generalized abstractions here.

## Common Pitfalls

### Pitfall 1: Canonical Grain Drift
**What goes wrong:** The project starts using both a 5-country spread panel and a 6-country macro panel interchangeably.
**Why it happens:** `collect_macro_data.py` currently keeps DE rows and uses `how="outer"`.
**How to avoid:** Declare the downstream canonical grain as non-DE `country` x `month_start`, and validate row counts after every merge.
**Warning signs:** `country == 'DE'` rows appear in a supposed modeling dataset, or row counts exceed `5 * months`.

### Pitfall 2: Trailing Partial Months Look Like Real Observations
**What goes wrong:** `2026-01` and `2026-02` are treated as valid training rows even though macro coverage is incomplete.
**Why it happens:** Yield data updates ahead of HICP and unemployment.
**How to avoid:** Compute and store a stable completeness cutoff. Current repo evidence says the last full non-DE month is `2025-12`.
**Warning signs:** Model input includes rows with missing HICP or unemployment in the latest months.

### Pitfall 3: Expected Rolling-Feature NaNs Get Misclassified as Data Errors
**What goes wrong:** The first month of `spread_change_1m` and first two months of `spread_vol_3m` are treated as broken data.
**Why it happens:** These are mathematically induced warm-up values, not missing source observations.
**How to avoid:** Track structural NaNs separately from source missingness.
**Warning signs:** Data-quality reports flag exactly 5 missing `spread_change_1m` and 10 missing `spread_vol_3m` as collector failures.

### Pitfall 4: ECB Series Keys Age Out Quietly
**What goes wrong:** A collector keeps returning data, but not the most current series coverage or dimension coding.
**Why it happens:** ECB migrated from SDW to the Data Portal, and current HICP portal metadata now exposes provider code `4D0` and notes methodological changes from 2026-02 onward.
**How to avoid:** Re-verify series keys against the current portal before locking Phase 1 outputs.
**Warning signs:** HICP coverage lags official release timing or differs across countries in unexpected ways.

### Pitfall 5: Live Verification Fails for Environmental Reasons
**What goes wrong:** A blocked socket or rate limit is mistaken for a code bug.
**Why it happens:** Sandbox networking is restricted, and public APIs can throttle.
**How to avoid:** Separate fixture tests from live smoke runs; record whether failures are code, network, or upstream.
**Warning signs:** `requests.exceptions.ConnectionError` without any parsing or schema errors.

## Code Examples

Verified patterns from official sources and current repo usage:

### ECB Data Retrieval with `startPeriod` and CSV Format
```python
# Source: https://data.ecb.europa.eu/help/api/data
url = "https://data-api.ecb.europa.eu/service/data/IRS/M.DE.L.L40.CI.0000.EUR.N.Z"
params = {"format": "csvdata", "startPeriod": "2019-01"}
resp = requests.get(url, params=params, timeout=30)
resp.raise_for_status()
```

### Eurostat SDMX 2.1 Dataset URL Pattern
```python
# Source: https://ec.europa.eu/eurostat/de/web/user-guides/data-browser/api-data-access/api-getting-started/sdmx2.1
url = (
    "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/"
    "une_rt_m/M.SA.TOTAL.PC_ACT.T.EL"
)
resp = requests.get(url, params={"format": "SDMX-CSV", "startPeriod": "2019-01"}, timeout=30)
resp.raise_for_status()
```

### Stable Window Assertion
```python
# Source: repo evidence from 2026-03-29 live run
non_de = panel[panel["country"] != "DE"].copy()
assert non_de.groupby("date")[feature_cols].apply(lambda x: x.notna().all().all()).loc[: "2025-12-01"].all()
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| ECB SDW endpoint and redirection reliance | Use `https://data-api.ecb.europa.eu/service/` directly | ECB says SDW redirections ended on 2025-10-01 | Current repo is correct on base URL; future work should not reintroduce SDW links |
| Treat latest pulled month as modeling-ready | Separate freshest collected month from stable complete window | Required by current source-update mismatch observed on 2026-03-29 | Prevents silent leakage of partial observations |
| Implicit HICP key assumptions from older notes | Re-check current portal metadata before locking the HICP series | Portal and methodology updates noted in 2026 official materials | Reduces risk of stale or partially updated HICP coverage |

**Deprecated/outdated:**
- Relying on ECB SDW redirect behavior: official ECB help says the redirections ended on 2025-10-01.

## Open Questions

1. **Should Germany macro variables become explicit benchmark features or remain out of the canonical row-level panel?**
   - What we know: current spread features already use German yields as a benchmark, and DE exists as macro-only rows today.
   - What's unclear: whether later modeling needs DE inflation and unemployment as separate covariates.
   - Recommendation: keep the canonical row grain non-DE either way; if DE macro is needed, merge it as renamed benchmark columns, not as extra rows.

2. **Should Phase 1 switch the HICP key from `.4.ANR` to the current portal’s `4D0` provider coding?**
   - What we know: the live collector works, but current portal pages show HICP series keys with `4D0`, and the repo fetch only yields 84 HICP months per country.
   - What's unclear: whether the current query is hitting a backward-compatible alias or a lagging series.
   - Recommendation: make this an explicit Phase 1 verification task before freezing the stabilized dataset.

3. **Should the stabilized output be a new file or a stricter contract over `macro_features.csv`?**
   - What we know: current `macro_features.csv` is useful diagnostically but not safe as a final modeling input.
   - What's unclear: whether the team wants an additional artifact such as `data/processed/panel_phase1.csv` or a validation manifest plus existing files.
   - Recommendation: create a distinct stabilized artifact to avoid ambiguity later.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python | Collection scripts | ? | 3.13.12 | — |
| `.venv` local environment | Script execution | ? | active project venv | System Python only if explicitly chosen |
| pandas | Collection and merge logic | ? | 3.0.1 | — |
| requests | API access | ? | 2.33.0 | — |
| ECB HTTPS access | Live bond and HICP collection | ? outside sandbox | live | Use checked-in CSVs or recorded fixtures when sandbox blocks outbound traffic |
| Eurostat HTTPS access | Live unemployment collection | ? outside sandbox | live | Use checked-in CSVs or recorded fixtures when sandbox blocks outbound traffic |
| pytest | Phase 1 regression tests | ? | — | Manual smoke runs only, which is weaker |
| Quarto | Later reporting | ? | 1.9.36 | — |
| scikit-learn | Phase 2 baselines | ? | — | Install in later phase |
| PyTorch | Phase 4 MLP | ? | — | Install in later phase |

**Missing dependencies with no fallback:**
- None for Phase 1 execution itself.

**Missing dependencies with fallback:**
- `pytest` is missing; manual script runs are possible, but fixture-backed validation is not.
- `scikit-learn` and `torch` are missing, but they do not block Phase 1.

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | none currently; recommend `pytest` for this phase |
| Config file | none |
| Quick run command | `.\.venv\Scripts\python.exe src/data_collection/collect_bond_yields.py` |
| Full suite command | `.\.venv\Scripts\python.exe src/data_collection/collect_bond_yields.py` then `.\.venv\Scripts\python.exe src/data_collection/collect_macro_data.py` |

### Phase Requirements -> Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| DATA-01 | ECB yield collector fetches all six source countries and emits 86 months per modeled country with no source missingness | smoke now, fixture-backed unit later | `.\.venv\Scripts\python.exe src/data_collection/collect_bond_yields.py` | ? Wave 0 |
| DATA-02 | Macro collector merges HICP and unemployment onto the country-month panel and reports coverage/missingness correctly | smoke now, fixture-backed integration later | `.\.venv\Scripts\python.exe src/data_collection/collect_macro_data.py` | ? Wave 0 |

### Sampling Rate

- **Per task commit:** run the smallest affected collector or validation script
- **Per wave merge:** run both collectors plus panel validation summary
- **Phase gate:** both live smoke runs and fixture-backed checks pass, and the stable cutoff is documented as data not assumption

### Wave 0 Gaps

- [ ] Install `pytest`: `.\.venv\Scripts\python.exe -m pip install pytest`
- [ ] Add `tests/data_collection/test_collect_bond_yields.py` with recorded ECB CSV fixtures
- [ ] Add `tests/data_collection/test_collect_macro_data.py` with recorded ECB and Eurostat CSV fixtures
- [ ] Add a panel-validation script or test that asserts canonical row count, duplicate-free keys, expected structural NaNs, and `2025-12` as the last complete non-DE month
- [ ] Add a small dependency manifest (`requirements.txt` or `pyproject.toml`) so environment recreation is not implicit

## Sources

### Primary (HIGH confidence)

- Repo inspection and live execution on 2026-03-29:
  - `src/data_collection/collect_bond_yields.py`
  - `src/data_collection/collect_macro_data.py`
  - `data/processed/bond_yields.csv`
  - `data/processed/macro_features.csv`
  - `CLAUDE.md`
  - `.planning/ROADMAP.md`
  - `.planning/REQUIREMENTS.md`
- ECB Data Portal API overview: https://data.ecb.europa.eu/help/api
- ECB Data API data-query syntax: https://data.ecb.europa.eu/help/api/data
- ECB Data Portal web-services overview: https://data.ecb.europa.eu/help/getting-data-web-services-sdmx-0
- Eurostat SDMX 2.1 API guide: https://ec.europa.eu/eurostat/de/web/user-guides/data-browser/api-data-access/api-getting-started/sdmx2.1
- ECB HICP dataset page showing current series metadata and update timing: https://data.ecb.europa.eu/data/datasets/HICP
- Eurostat inflation release noting February 2026 methodological changes: https://ec.europa.eu/eurostat/web/products-euro-indicators/w/2-18032026-ap

### Secondary (MEDIUM confidence)

- None.

### Tertiary (LOW confidence)

- None.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - confirmed from the actual local environment and official API docs
- Architecture: HIGH - driven by repo outputs, live runs, and clear grain mismatch in the current merge artifact
- Pitfalls: HIGH - based on observed missingness patterns, current code paths, and official API migration/update notes

**Research date:** 2026-03-29
**Valid until:** 2026-04-28
