"""Statistical monitoring for AML.

Provides statistical anomaly detection for transaction monitoring
using robust statistics and sequential methods.
"""

from __future__ import annotations

from collections import deque
from datetime import datetime
from typing import TYPE_CHECKING, Any

import numpy as np
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from ununseptium.aml.transactions import Transaction


class AnomalyResult(BaseModel):
    """Result of anomaly detection.

    Attributes:
        transaction_id: Transaction ID.
        is_anomaly: Whether transaction is anomalous.
        anomaly_score: Anomaly score (0.0 to 1.0).
        z_score: Standard deviation from mean.
        robust_score: MAD-based robust score.
        contributing_factors: Features contributing to anomaly.
        detected_at: Detection timestamp.
    """

    transaction_id: str
    is_anomaly: bool
    anomaly_score: float = Field(ge=0.0, le=1.0)
    z_score: float | None = None
    robust_score: float | None = None
    contributing_factors: list[str] = Field(default_factory=list)
    detected_at: datetime = Field(default_factory=datetime.utcnow)


class StatisticalMonitor:
    """Statistical anomaly detection for transactions.

    Uses robust statistics to detect unusual transactions:
    - Z-score based on trimmed mean and MAD
    - Huber loss for outlier resistance
    - Streaming statistics for online detection

    Example:
        ```python
        from ununseptium.aml.monitoring import StatisticalMonitor

        monitor = StatisticalMonitor(window_size=1000)

        # Train on historical data
        for txn in historical_transactions:
            monitor.update(txn)

        # Detect anomalies
        result = monitor.detect(new_transaction)
        if result.is_anomaly:
            print(f"Anomaly detected: {result.anomaly_score}")
        ```
    """

    def __init__(
        self,
        window_size: int = 1000,
        anomaly_threshold: float = 3.0,
        trim_fraction: float = 0.1,
    ) -> None:
        """Initialize the monitor.

        Args:
            window_size: Size of sliding window for statistics.
            anomaly_threshold: Z-score threshold for anomaly.
            trim_fraction: Fraction to trim from each end for robust mean.
        """
        self.window_size = window_size
        self.anomaly_threshold = anomaly_threshold
        self.trim_fraction = trim_fraction

        # Streaming statistics
        self._amounts: deque[float] = deque(maxlen=window_size)
        self._running_sum: float = 0.0
        self._running_sq_sum: float = 0.0
        self._count: int = 0

    def update(self, transaction: Transaction) -> None:
        """Update statistics with a transaction.

        Args:
            transaction: Transaction to incorporate.
        """
        amount = float(transaction.amount)

        if len(self._amounts) >= self.window_size:
            old_amount = self._amounts[0]
            self._running_sum -= old_amount
            self._running_sq_sum -= old_amount * old_amount

        self._amounts.append(amount)
        self._running_sum += amount
        self._running_sq_sum += amount * amount
        self._count += 1

    def detect(self, transaction: Transaction) -> AnomalyResult:
        """Detect if a transaction is anomalous.

        Args:
            transaction: Transaction to evaluate.

        Returns:
            AnomalyResult with detection details.
        """
        amount = float(transaction.amount)
        contributing_factors: list[str] = []

        if len(self._amounts) < 10:
            # Not enough data
            return AnomalyResult(
                transaction_id=transaction.id,
                is_anomaly=False,
                anomaly_score=0.0,
            )

        # Calculate statistics
        amounts_array = np.array(list(self._amounts))

        # Standard z-score
        mean = np.mean(amounts_array)
        std = np.std(amounts_array)
        z_score = abs((amount - mean) / std) if std > 0 else 0.0

        # Robust z-score using MAD
        median = np.median(amounts_array)
        mad = np.median(np.abs(amounts_array - median))
        mad_scale = 1.4826  # Scale factor for normal distribution
        robust_mad = mad * mad_scale
        robust_score = abs((amount - median) / robust_mad) if robust_mad > 0 else 0.0

        # Trimmed mean z-score
        n = len(amounts_array)
        trim_n = int(n * self.trim_fraction)
        sorted_amounts = np.sort(amounts_array)
        trimmed = sorted_amounts[trim_n : n - trim_n] if trim_n > 0 else sorted_amounts
        trimmed_mean = np.mean(trimmed)
        trimmed_std = np.std(trimmed)
        trimmed_z = abs((amount - trimmed_mean) / trimmed_std) if trimmed_std > 0 else 0.0

        # Combined score (weighted)
        anomaly_score = 0.3 * min(z_score / self.anomaly_threshold, 1.0)
        anomaly_score += 0.4 * min(robust_score / self.anomaly_threshold, 1.0)
        anomaly_score += 0.3 * min(trimmed_z / self.anomaly_threshold, 1.0)
        anomaly_score = min(anomaly_score, 1.0)

        is_anomaly = (
            z_score > self.anomaly_threshold
            or robust_score > self.anomaly_threshold
            or trimmed_z > self.anomaly_threshold
        )

        if z_score > self.anomaly_threshold:
            contributing_factors.append(f"z_score={z_score:.2f}")
        if robust_score > self.anomaly_threshold:
            contributing_factors.append(f"robust_score={robust_score:.2f}")
        if trimmed_z > self.anomaly_threshold:
            contributing_factors.append(f"trimmed_z={trimmed_z:.2f}")

        # Check for round amounts (common in structuring)
        if amount > 0 and amount % 1000 == 0:
            contributing_factors.append("round_amount")
            anomaly_score = min(anomaly_score + 0.1, 1.0)

        return AnomalyResult(
            transaction_id=transaction.id,
            is_anomaly=is_anomaly,
            anomaly_score=round(anomaly_score, 4),
            z_score=round(z_score, 4),
            robust_score=round(robust_score, 4),
            contributing_factors=contributing_factors,
        )

    def detect_batch(
        self,
        transactions: list[Transaction],
        *,
        update_stats: bool = True,
    ) -> list[AnomalyResult]:
        """Detect anomalies in a batch of transactions.

        Args:
            transactions: Transactions to evaluate.
            update_stats: Whether to update statistics.

        Returns:
            List of AnomalyResults.
        """
        results: list[AnomalyResult] = []

        for txn in transactions:
            result = self.detect(txn)
            results.append(result)

            if update_stats:
                self.update(txn)

        return results

    def get_statistics(self) -> dict[str, Any]:
        """Get current statistics summary.

        Returns:
            Dictionary with statistical summaries.
        """
        if not self._amounts:
            return {"count": 0, "mean": None, "std": None, "median": None}

        amounts_array = np.array(list(self._amounts))

        return {
            "count": len(self._amounts),
            "mean": float(np.mean(amounts_array)),
            "std": float(np.std(amounts_array)),
            "median": float(np.median(amounts_array)),
            "min": float(np.min(amounts_array)),
            "max": float(np.max(amounts_array)),
            "p25": float(np.percentile(amounts_array, 25)),
            "p75": float(np.percentile(amounts_array, 75)),
            "p95": float(np.percentile(amounts_array, 95)),
            "p99": float(np.percentile(amounts_array, 99)),
        }

    def reset(self) -> None:
        """Reset all statistics."""
        self._amounts.clear()
        self._running_sum = 0.0
        self._running_sq_sum = 0.0
        self._count = 0
