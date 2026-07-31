"""Predictive Risk Assessment Framework (PRAF)."""

__all__ = ["domain", "engine", "io", "config", "__version__", "MODEL_VERSION"]

# Version of the software package.
__version__ = "0.3.0"

# Version of the *risk model* itself: the indicator library, the weight tables
# (nature / base / activity-domain), the acceptability thresholds, and the
# control-effect semantics. This is deliberately separate from the package
# version and MUST be bumped whenever any of those scoring inputs change, so
# that a stored assessment can be traced back to the exact model that produced
# it (ISO 14971 traceability / reproducibility).
MODEL_VERSION = "risk-model-2026.2"

# Version of the report/audit-trail schema emitted by the engine.
SCHEMA_VERSION = "1.0"
