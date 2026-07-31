# Predictive-Risk-Assessment-Framework

Design-stage risk triage and decision-support for early-stage POCT device development.

> **Status: prototype (v0.2.0) — decision support only.** PRAF is a structured,
> explainable scoring tool for surfacing and prioritising risk early. It is
> **not** a validated medical-device risk system and does not replace a
> manufacturer's ISO 14971 risk file or design controls. Its indicators,
> weights, and thresholds are governance defaults, not clinically derived, and
> carry no validation evidence. See
> [`docs/iso/risk_management_approach.md`](docs/iso/risk_management_approach.md)
> for scope, acceptability criteria, and validation status.

## Repository layout

```text
.
├── README.md
├── LICENSE
├── pyproject.toml
├── requirements.txt
├── app.py                      # optional Streamlit app (needs the [app] extra)
├── src/praf/
│   ├── __init__.py             # __version__, MODEL_VERSION, SCHEMA_VERSION
│   ├── config/
│   │   ├── defaults.py         # scales + acceptability thresholds (40/70)
│   │   ├── schemas.py
│   │   └── validation.py       # input-completeness + threshold/weight checks
│   ├── domain/
│   │   ├── activities.py       # activities, project stages, context
│   │   ├── domains.py          # 7 risk domains + activity domain weights
│   │   ├── categories.py
│   │   ├── natures.py
│   │   ├── indicators.py       # built-in indicator library (I001–I012)
│   │   └── risk_patterns.py
│   ├── engine/
│   │   ├── scorer.py           # per-indicator scoring (polarity, 1–5 axes)
│   │   ├── aggregator.py       # 0–100 domain/category indices
│   │   ├── classifier.py       # acceptable / action / escalation bands
│   │   ├── severity_guard.py   # catastrophic-impact backstop (never lowers)
│   │   ├── rules.py            # proceed / revise / escalate decision
│   │   ├── pipeline.py         # end-to-end orchestration (used by the CLI)
│   │   ├── explainability.py   # top contributors per domain
│   │   ├── guidance.py         # pattern-based gate guidance (Streamlit app)
│   │   └── audit_trail.py      # provenance: timestamp, versions, thresholds
│   ├── io/
│   │   ├── loaders.py          # validated JSON input loading
│   │   └── exporters.py        # atomic JSON report export
│   └── cli/main.py
├── data/examples/
│   ├── example_inputs.json
│   └── templates/              # illustrative CSV shapes (see note below)
├── docs/iso/
│   ├── risk_management_approach.md
│   └── scoring_method.md
├── scripts/generate_example_outputs.py
└── tests/                      # 9 test modules, engine + IO + CLI
```

## Installation

The core scoring engine has no third-party dependencies:

```bash
pip install -e .
```

The interactive app needs the optional `app` extra:

```bash
pip install -e ".[app]"
```

## Usage

Run the scoring pipeline on a JSON input file (see `data/examples/example_inputs.json`):

```bash
python -m praf.cli.main data/examples/example_inputs.json          # print report
python -m praf.cli.main data/examples/example_inputs.json out.json # also write it
```

The report includes an `input_completeness` block and any `severity_overrides`;
incomplete input is scored (missing values default to neutral) but flagged on
stderr and in the report. Run `python -m praf.cli.main --help` for usage.

Launch the interactive app (requires the `[app]` extra):

```bash
streamlit run app.py
```

> The CSV files under `data/examples/templates/` are **illustrative examples** of
> the indicator/weight shape. A CSV import path for custom libraries/weights is
> not yet wired into the engine; scoring today uses the built-in library.

Regenerate the example output (writes `data/examples/example_outputs.json`,
which is generated on demand and not tracked in git):

```bash
python scripts/generate_example_outputs.py
```

## Tests

```bash
pip install -e ".[dev]"
pytest
```
