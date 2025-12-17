"""Mathematical and statistical methods module.

Provides advanced statistical methods for risk analysis:
- Uncertainty quantification (conformal prediction)
- Sequential detection (CUSUM, SPRT, ADWIN)
- Extreme value theory (GPD)
- Point processes (Hawkes)
- Dependence modeling (copulas)
- Graph statistics
"""

from ununseptium.mathstats.dependence import CopulaFitter, DependenceMetrics
from ununseptium.mathstats.graphstats import (
    CommunityDetector,
    GraphFeatures,
    TemporalMotifs,
)
from ununseptium.mathstats.numerics import NumericsUtils
from ununseptium.mathstats.point_process import HawkesProcess, IntensityEstimator
from ununseptium.mathstats.sequential import ADWIN, CUSUM, SPRT, DriftDetector
from ununseptium.mathstats.tails import EVTAnalyzer, GPDFit, TailRiskScore
from ununseptium.mathstats.uncertainty import (
    CalibrationMetrics,
    ConformalPredictor,
    PredictionSet,
)

__all__ = [
    # Sequential
    "ADWIN",
    "CUSUM",
    "SPRT",
    # Uncertainty
    "CalibrationMetrics",
    # Graph Stats
    "CommunityDetector",
    "ConformalPredictor",
    # Dependence
    "CopulaFitter",
    "DependenceMetrics",
    "DriftDetector",
    # Tails
    "EVTAnalyzer",
    "GPDFit",
    "GraphFeatures",
    # Point Process
    "HawkesProcess",
    "IntensityEstimator",
    # Numerics
    "NumericsUtils",
    "PredictionSet",
    "TailRiskScore",
    "TemporalMotifs",
]
