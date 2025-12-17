"""Point process models for event analysis.

Provides Hawkes process modeling for self-exciting events.
"""

from __future__ import annotations

import numpy as np
from pydantic import BaseModel, Field


class HawkesParameters(BaseModel):
    """Hawkes process parameters.

    Attributes:
        mu: Background intensity.
        alpha: Excitation jump.
        beta: Decay rate.
    """

    mu: float = Field(gt=0)
    alpha: float = Field(ge=0, lt=1)  # alpha < beta for stability
    beta: float = Field(gt=0)

    @property
    def branching_ratio(self) -> float:
        """Branching ratio alpha/beta (must be < 1 for stationarity)."""
        return self.alpha / self.beta if self.beta > 0 else float("inf")


class IntensityResult(BaseModel):
    """Intensity estimation result.

    Attributes:
        time: Time point.
        intensity: Intensity value.
        background: Background component.
        excitation: Excitation component.
    """

    time: float
    intensity: float
    background: float
    excitation: float


class HawkesProcess:
    """Univariate Hawkes process model.

    Self-exciting point process for modeling event clustering.

    Mathematical Foundation:
        Conditional intensity:
        lambda(t) = mu + sum_{t_i < t} alpha * exp(-beta * (t - t_i))

        The process is stationary if alpha < beta (branching ratio < 1).

    Example:
        ```python
        from ununseptium.mathstats import HawkesProcess
        import numpy as np

        # Fit to event times
        events = np.array([0.1, 0.5, 0.6, 1.2, 2.0, 2.1, 2.15])

        hawkes = HawkesProcess()
        params = hawkes.fit(events, T=3.0)
        print(f"Branching ratio: {params.branching_ratio}")

        # Compute intensity at time t
        intensity = hawkes.intensity(2.5, events)
        ```
    """

    def __init__(
        self,
        mu: float = 1.0,
        alpha: float = 0.5,
        beta: float = 1.0,
    ) -> None:
        """Initialize Hawkes process.

        Args:
            mu: Background intensity.
            alpha: Excitation jump.
            beta: Decay rate.
        """
        self._params = HawkesParameters(mu=mu, alpha=alpha, beta=beta)

    @property
    def params(self) -> HawkesParameters:
        """Current parameters."""
        return self._params

    def intensity(
        self,
        t: float,
        events: np.ndarray,
    ) -> float:
        """Compute intensity at time t.

        Args:
            t: Time point.
            events: Array of event times.

        Returns:
            Intensity value.
        """
        mu = self._params.mu
        alpha = self._params.alpha
        beta = self._params.beta

        # Sum excitation from past events
        past_events = events[events < t]
        if len(past_events) == 0:
            return mu

        excitation = alpha * np.sum(np.exp(-beta * (t - past_events)))
        return mu + excitation

    def intensity_trajectory(
        self,
        times: np.ndarray,
        events: np.ndarray,
    ) -> list[IntensityResult]:
        """Compute intensity trajectory.

        Args:
            times: Time points to evaluate.
            events: Array of event times.

        Returns:
            List of IntensityResults.
        """
        results = []
        mu = self._params.mu
        alpha = self._params.alpha
        beta = self._params.beta

        for t in times:
            past_events = events[events < t]
            if len(past_events) == 0:
                excitation = 0.0
            else:
                excitation = alpha * np.sum(np.exp(-beta * (t - past_events)))

            results.append(
                IntensityResult(
                    time=float(t),
                    intensity=mu + excitation,
                    background=mu,
                    excitation=excitation,
                )
            )

        return results

    def fit(
        self,
        events: np.ndarray,
        T: float,
        *,
        method: str = "mle",
    ) -> HawkesParameters:
        """Fit parameters to event data.

        Args:
            events: Array of event times.
            T: Observation window [0, T].
            method: Fitting method ('mle' or 'moment').

        Returns:
            Fitted HawkesParameters.
        """
        if method == "moment":
            return self._fit_moment(events, T)
        return self._fit_mle(events, T)

    def _fit_mle(self, events: np.ndarray, T: float) -> HawkesParameters:
        """Maximum likelihood estimation."""
        from scipy.optimize import minimize

        n = len(events)
        if n < 2:
            return self._params

        def neg_log_likelihood(params: np.ndarray) -> float:
            mu, alpha, beta = params

            if mu <= 0 or alpha < 0 or beta <= 0 or alpha >= beta:
                return 1e10

            # Compute log-likelihood
            ll = 0.0

            # Sum of log-intensities at event times
            for i, ti in enumerate(events):
                past = events[:i]
                if len(past) == 0:
                    intensity = mu
                else:
                    intensity = mu + alpha * np.sum(np.exp(-beta * (ti - past)))

                if intensity > 0:
                    ll += np.log(intensity)
                else:
                    return 1e10

            # Integral of intensity
            ll -= mu * T

            for ti in events:
                ll -= (alpha / beta) * (1 - np.exp(-beta * (T - ti)))

            return -ll

        # Initial guess
        x0 = np.array([
            self._params.mu,
            self._params.alpha,
            self._params.beta,
        ])

        # Optimize
        result = minimize(
            neg_log_likelihood,
            x0,
            method="L-BFGS-B",
            bounds=[(1e-6, None), (0, None), (1e-6, None)],
        )

        if result.success:
            mu, alpha, beta = result.x
            # Ensure stability
            if alpha >= beta:
                alpha = 0.9 * beta
            self._params = HawkesParameters(mu=mu, alpha=alpha, beta=beta)

        return self._params

    def _fit_moment(self, events: np.ndarray, T: float) -> HawkesParameters:
        """Method of moments estimation."""
        n = len(events)
        if n < 2:
            return self._params

        # Mean rate
        mean_rate = n / T

        # Inter-event times
        inter_times = np.diff(events)
        mean_inter = np.mean(inter_times)
        var_inter = np.var(inter_times)

        # Estimate branching ratio from clustering
        cv_squared = var_inter / (mean_inter**2) if mean_inter > 0 else 1.0
        branching = max(0, min(0.9, 1 - 1 / cv_squared)) if cv_squared > 1 else 0.1

        # Background rate
        mu = mean_rate * (1 - branching)

        # Decay rate (heuristic)
        beta = 1.0 / mean_inter if mean_inter > 0 else 1.0
        alpha = branching * beta

        self._params = HawkesParameters(mu=mu, alpha=alpha, beta=beta)
        return self._params

    def simulate(
        self,
        T: float,
        *,
        seed: int | None = None,
    ) -> np.ndarray:
        """Simulate event times via thinning.

        Args:
            T: Simulation horizon.
            seed: Random seed.

        Returns:
            Array of simulated event times.
        """
        if seed is not None:
            np.random.seed(seed)

        mu = self._params.mu
        alpha = self._params.alpha
        beta = self._params.beta

        events = []
        t = 0.0

        # Upper bound on intensity
        lambda_upper = mu + alpha * len(events) if events else mu

        while t < T:
            # Next candidate time
            lambda_upper = max(mu, lambda_upper)
            dt = np.random.exponential(1 / lambda_upper)
            t += dt

            if t >= T:
                break

            # Compute actual intensity
            event_array = np.array(events) if events else np.array([])
            lambda_t = self.intensity(t, event_array)

            # Accept/reject
            if np.random.random() < lambda_t / lambda_upper:
                events.append(t)
                lambda_upper = lambda_t + alpha

        return np.array(events)


class IntensityEstimator:
    """Non-parametric intensity estimation.

    Example:
        ```python
        from ununseptium.mathstats import IntensityEstimator

        estimator = IntensityEstimator(bandwidth=0.5)
        intensity = estimator.estimate(times, events)
        ```
    """

    def __init__(self, bandwidth: float = 1.0) -> None:
        """Initialize estimator.

        Args:
            bandwidth: Kernel bandwidth.
        """
        self.bandwidth = bandwidth

    def estimate(
        self,
        times: np.ndarray,
        events: np.ndarray,
    ) -> np.ndarray:
        """Estimate intensity using kernel smoothing.

        Args:
            times: Time points to evaluate.
            events: Event times.

        Returns:
            Estimated intensity values.
        """
        h = self.bandwidth
        intensities = np.zeros(len(times))

        for i, t in enumerate(times):
            # Count events in kernel window
            weights = np.exp(-((t - events) ** 2) / (2 * h**2))
            weights = weights[events <= t]  # Only past events
            intensities[i] = np.sum(weights) / (h * np.sqrt(2 * np.pi))

        return intensities

    def cumulative(
        self,
        events: np.ndarray,
        T: float,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Compute cumulative intensity (compensator).

        Args:
            events: Event times.
            T: Observation horizon.

        Returns:
            Tuple of (times, cumulative intensity).
        """
        times = np.linspace(0, T, 100)
        intensity = self.estimate(times, events)
        cumulative = np.cumsum(intensity) * (times[1] - times[0])

        return times, cumulative
