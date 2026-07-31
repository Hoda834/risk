"""End-to-end orchestration of the indicator-based assessment.

Centralises the score -> aggregate -> classify -> severity-guard -> decide ->
explain -> audit flow so both the CLI and any test/embedding use one code path
(previously the CLI inlined all of this and read the input file twice).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from praf.domain import INDICATOR_LIBRARY, Context
from praf.domain.domains import activity_domain_weights
from praf.config.defaults import Defaults
from praf.config.validation import validate_inputs, validate_domain_weights, InputValidationReport
from praf.engine.scorer import score_indicators
from praf.engine.aggregator import aggregate_scores
from praf.engine.classifier import classify_domains
from praf.engine.severity_guard import apply_severity_guard, SeverityGuardResult
from praf.engine.rules import decide
from praf.engine.explainability import explain
from praf.engine.audit_trail import build_audit_trail


@dataclass(frozen=True)
class AssessmentResult:
    report: Dict[str, Any]
    validation: InputValidationReport
    severity_guard: SeverityGuardResult


def run_assessment(
    responses: Dict[str, Any],
    likelihood: Dict[str, Any],
    impact: Dict[str, Any],
    detectability: Dict[str, Any],
    context: Context,
    defaults: Optional[Defaults] = None,
    *,
    top_n: int = 5,
    generated_at: Optional[str] = None,
) -> AssessmentResult:
    defaults = defaults or Defaults()

    validation = validate_inputs(
        list(INDICATOR_LIBRARY.keys()), responses, likelihood, impact, detectability
    )

    domain_weights = activity_domain_weights(context.activity)
    validate_domain_weights(domain_weights)

    scored = score_indicators(
        responses=responses,
        likelihood=likelihood,
        impact=impact,
        detectability=detectability,
        domain_weights=domain_weights,
    )

    aggregated = aggregate_scores(scored.indicator_details, scored.local_scores)
    classifications = classify_domains(
        aggregated.domain_scores, defaults.low_threshold, defaults.high_threshold
    )

    guard = apply_severity_guard(classifications, scored.indicator_details)
    classifications = guard.classifications

    decision = decide(classifications)
    expl = explain(classifications, scored.indicator_details, scored.local_scores, top_n=top_n)

    ctx_dict = {"activity": context.activity.value, "stage": context.stage.value}
    thresholds = {"low": defaults.low_threshold, "high": defaults.high_threshold}

    audit = build_audit_trail(
        classifications,
        decision,
        scored.indicator_details,
        scored.local_scores,
        context=ctx_dict,
        thresholds=thresholds,
        input_completeness=validation.as_dict(),
        severity_overrides=guard.overrides,
        generated_at=generated_at,
    )

    report: Dict[str, Any] = {
        "context": ctx_dict,
        "input_completeness": validation.as_dict(),
        "overall_decision": decision.overall.value,
        "per_domain_decision": {d.value: decision.per_domain[d].value for d in decision.per_domain},
        "domain_scores": {
            d.value: {"score": classifications[d].score, "level": classifications[d].level.value}
            for d in classifications
        },
        "severity_overrides": [
            {
                "domain": o.domain.value,
                "indicator_id": o.indicator_id,
                "from_level": o.from_level.value,
                "to_level": o.to_level.value,
                "reason": o.reason,
            }
            for o in guard.overrides
        ],
        "top_contributors_by_domain": {
            d.value: expl.top_contributors_by_domain.get(d, []) for d in classifications
        },
        "audit_trail": [{"key": a.key, "value": a.value} for a in audit],
    }

    return AssessmentResult(report=report, validation=validation, severity_guard=guard)
