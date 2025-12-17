"""Streaming monitoring for AML.

Provides real-time transaction monitoring with O(1) memory
streaming algorithms.
"""

from __future__ import annotations

from collections import deque
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from ununseptium.aml.transactions import Transaction


class StreamingAlert(BaseModel):
    """An alert from streaming monitoring.

    Attributes:
        alert_type: Type of alert.
        transaction_id: Triggering transaction ID.
        entity_id: Related entity ID.
        score: Alert score.
        reason: Alert reason.
        threshold_value: Threshold that was exceeded.
        actual_value: Actual observed value.
        window_size: Time window for detection.
        detected_at: Detection timestamp.
    """

    alert_type: str
    transaction_id: str
    entity_id: str | None = None
    score: float = Field(ge=0.0, le=1.0)
    reason: str
    threshold_value: float | None = None
    actual_value: float | None = None
    window_size: timedelta | None = None
    detected_at: datetime = Field(default_factory=datetime.utcnow)


class VelocityTracker:
    """Track transaction velocity per entity.

    Maintains O(1) memory by using time-bucketed counters.
    """

    def __init__(
        self,
        window: timedelta = timedelta(hours=24),
        bucket_size: timedelta = timedelta(hours=1),
    ) -> None:
        """Initialize the tracker.

        Args:
            window: Time window for velocity calculation.
            bucket_size: Size of time buckets.
        """
        self.window = window
        self.bucket_size = bucket_size
        self._buckets: dict[str, deque[tuple[datetime, int, float]]] = {}

    def record(
        self,
        entity_id: str,
        timestamp: datetime,
        amount: float,
    ) -> None:
        """Record a transaction for an entity.

        Args:
            entity_id: Entity identifier.
            timestamp: Transaction timestamp.
            amount: Transaction amount.
        """
        if entity_id not in self._buckets:
            max_buckets = int(self.window / self.bucket_size) + 1
            self._buckets[entity_id] = deque(maxlen=max_buckets)

        buckets = self._buckets[entity_id]

        # Get bucket timestamp
        bucket_ts = self._bucket_timestamp(timestamp)

        # Update or add bucket
        if buckets and buckets[-1][0] == bucket_ts:
            old_ts, old_count, old_amount = buckets[-1]
            buckets[-1] = (old_ts, old_count + 1, old_amount + amount)
        else:
            buckets.append((bucket_ts, 1, amount))

        # Prune old buckets
        self._prune(entity_id, timestamp)

    def get_velocity(
        self,
        entity_id: str,
        timestamp: datetime | None = None,
    ) -> tuple[int, float]:
        """Get transaction velocity for an entity.

        Args:
            entity_id: Entity identifier.
            timestamp: Reference timestamp (default: now).

        Returns:
            Tuple of (transaction_count, total_amount).
        """
        if timestamp is None:
            timestamp = datetime.now(timezone.utc)

        if entity_id not in self._buckets:
            return 0, 0.0

        self._prune(entity_id, timestamp)

        buckets = self._buckets[entity_id]
        cutoff = timestamp - self.window

        total_count = 0
        total_amount = 0.0

        for bucket_ts, count, amount in buckets:
            if bucket_ts >= cutoff:
                total_count += count
                total_amount += amount

        return total_count, total_amount

    def _bucket_timestamp(self, timestamp: datetime) -> datetime:
        """Get the bucket timestamp for a given timestamp."""
        bucket_seconds = int(self.bucket_size.total_seconds())
        ts_seconds = int(timestamp.timestamp())
        bucket_ts = ts_seconds - (ts_seconds % bucket_seconds)
        return datetime.fromtimestamp(bucket_ts)

    def _prune(self, entity_id: str, timestamp: datetime) -> None:
        """Remove expired buckets."""
        if entity_id not in self._buckets:
            return

        buckets = self._buckets[entity_id]
        cutoff = timestamp - self.window - self.bucket_size

        while buckets and buckets[0][0] < cutoff:
            buckets.popleft()


class StreamingMonitor:
    """Real-time streaming monitor for transactions.

    Provides O(1) memory streaming algorithms for:
    - Velocity monitoring
    - Amount threshold monitoring
    - Pattern detection

    Example:
        ```python
        from ununseptium.aml.monitoring import StreamingMonitor

        monitor = StreamingMonitor()

        # Process transactions in real-time
        for txn in transaction_stream:
            alerts = monitor.process(txn)
            for alert in alerts:
                handle_alert(alert)
        ```
    """

    def __init__(
        self,
        velocity_window: timedelta = timedelta(hours=24),
        velocity_threshold: int = 20,
        amount_threshold: float = 50000.0,
        cumulative_threshold: float = 100000.0,
    ) -> None:
        """Initialize the streaming monitor.

        Args:
            velocity_window: Time window for velocity tracking.
            velocity_threshold: Max transactions per window.
            amount_threshold: Single transaction amount threshold.
            cumulative_threshold: Cumulative amount threshold per window.
        """
        self.velocity_window = velocity_window
        self.velocity_threshold = velocity_threshold
        self.amount_threshold = amount_threshold
        self.cumulative_threshold = cumulative_threshold

        self._velocity_tracker = VelocityTracker(
            window=velocity_window,
            bucket_size=timedelta(hours=1),
        )

    def process(self, transaction: Transaction) -> list[StreamingAlert]:
        """Process a transaction and generate alerts.

        Args:
            transaction: Transaction to process.

        Returns:
            List of generated alerts.
        """
        alerts: list[StreamingAlert] = []

        sender_id = transaction.sender.id if transaction.sender else transaction.sender_id
        receiver_id = transaction.receiver.id if transaction.receiver else transaction.receiver_id
        amount = float(transaction.amount)
        timestamp = transaction.timestamp

        # Single transaction amount check
        if amount >= self.amount_threshold:
            alerts.append(
                StreamingAlert(
                    alert_type="high_value_transaction",
                    transaction_id=transaction.id,
                    entity_id=sender_id,
                    score=min(amount / (self.amount_threshold * 2), 1.0),
                    reason=f"Transaction amount {amount} exceeds threshold",
                    threshold_value=self.amount_threshold,
                    actual_value=amount,
                )
            )

        # Velocity checks
        for entity_id in [sender_id, receiver_id]:
            if not entity_id:
                continue

            # Record transaction
            self._velocity_tracker.record(entity_id, timestamp, amount)

            # Check velocity
            count, total = self._velocity_tracker.get_velocity(entity_id, timestamp)

            if count >= self.velocity_threshold:
                alerts.append(
                    StreamingAlert(
                        alert_type="velocity_exceeded",
                        transaction_id=transaction.id,
                        entity_id=entity_id,
                        score=min(count / (self.velocity_threshold * 2), 1.0),
                        reason=f"Transaction count {count} exceeds threshold",
                        threshold_value=float(self.velocity_threshold),
                        actual_value=float(count),
                        window_size=self.velocity_window,
                    )
                )

            if total >= self.cumulative_threshold:
                alerts.append(
                    StreamingAlert(
                        alert_type="cumulative_amount_exceeded",
                        transaction_id=transaction.id,
                        entity_id=entity_id,
                        score=min(total / (self.cumulative_threshold * 2), 1.0),
                        reason=f"Cumulative amount {total} exceeds threshold",
                        threshold_value=self.cumulative_threshold,
                        actual_value=total,
                        window_size=self.velocity_window,
                    )
                )

        return alerts

    def process_batch(
        self,
        transactions: list[Transaction],
    ) -> list[StreamingAlert]:
        """Process a batch of transactions.

        Args:
            transactions: Transactions to process.

        Returns:
            All generated alerts.
        """
        all_alerts: list[StreamingAlert] = []

        for txn in transactions:
            alerts = self.process(txn)
            all_alerts.extend(alerts)

        return all_alerts

    def get_entity_stats(
        self,
        entity_id: str,
        timestamp: datetime | None = None,
    ) -> dict[str, Any]:
        """Get statistics for an entity.

        Args:
            entity_id: Entity identifier.
            timestamp: Reference timestamp.

        Returns:
            Entity statistics.
        """
        count, total = self._velocity_tracker.get_velocity(entity_id, timestamp)

        return {
            "entity_id": entity_id,
            "transaction_count": count,
            "total_amount": total,
            "window": str(self.velocity_window),
        }
