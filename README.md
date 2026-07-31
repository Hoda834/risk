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
predictive-risk-assessment-framework/
  README.md
  LICENSE
  pyproject.toml
  .gitignore
  src/
    praf/
      __init__.py
      config/
        __init__.py
        defaults.py
        schemas.py
        validation.py
      domain/
        __init__.py
        activities.py
        domains.py
        natures.py
        categories.py
        indicators.py
        risk_patterns.py
      engine/
        __init__.py
        scorer.py
        aggregator.py
        classifier.py
        severity_guard.py
        rules.py
        pipeline.py
        explainability.py
        guidance.py
        audit_trail.py
      io/
        __init__.py
        loaders.py
        exporters.py
      cli/
        __init__.py
        main.py
  data/
    templates/
      indicator_library_template.csv
      weights_template.csv
    examples/
      example_inputs.json
  docs/
    iso/
      risk_management_approach.md
      scoring_method.md
  tests/
    test_scorer.py
    test_classifier.py
    test_pipeline.py
    test_validation.py
    test_severity_guard.py
    test_aggregator.py
    test_audit_trail.py
    test_io.py
    test_cli.py
  scripts/
    generate_example_outputs.py

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
stderr and in the report.

Launch the interactive app:

```bash
streamlit run app.py
```

> The CSV files under `data/examples/templates/` are **illustrative examples** of
> the indicator/weight shape. A CSV import path for custom libraries/weights is
> not yet wired into the engine; scoring today uses the built-in library.

Regenerate the example output:

```bash
python scripts/generate_example_outputs.py
```

## Tests

```bash
pip install pytest
pytest
```
