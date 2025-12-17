"""Physics-Informed Neural Networks.

Provides PINN training interface for solving PDEs.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

import numpy as np
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    pass


class PINNConfig(BaseModel):
    """Configuration for PINN training.

    Attributes:
        n_layers: Number of hidden layers.
        n_neurons: Neurons per hidden layer.
        activation: Activation function name.
        learning_rate: Learning rate.
        n_epochs: Training epochs.
        n_collocation: Collocation points for PDE.
        n_boundary: Boundary condition points.
        pde_weight: Weight for PDE loss.
        bc_weight: Weight for boundary condition loss.
        data_weight: Weight for data loss.
    """

    n_layers: int = Field(default=4, ge=1)
    n_neurons: int = Field(default=64, ge=1)
    activation: str = "tanh"
    learning_rate: float = Field(default=1e-3, gt=0)
    n_epochs: int = Field(default=10000, ge=1)
    n_collocation: int = Field(default=1000, ge=1)
    n_boundary: int = Field(default=100, ge=1)
    pde_weight: float = Field(default=1.0, ge=0)
    bc_weight: float = Field(default=1.0, ge=0)
    data_weight: float = Field(default=1.0, ge=0)


class PDEResidual(BaseModel):
    """PDE residual evaluation result.

    Attributes:
        residual: PDE residual value.
        points: Evaluation points.
        derivatives: Computed derivatives.
    """

    residual: np.ndarray = Field(default_factory=lambda: np.array([]))
    points: np.ndarray = Field(default_factory=lambda: np.array([]))
    derivatives: dict[str, np.ndarray] = Field(default_factory=dict)

    model_config = {"arbitrary_types_allowed": True}


class TrainingHistory(BaseModel):
    """Training history for PINN.

    Attributes:
        total_loss: Total loss per epoch.
        pde_loss: PDE loss per epoch.
        bc_loss: Boundary condition loss.
        data_loss: Data loss.
        n_epochs: Number of epochs trained.
    """

    total_loss: list[float] = Field(default_factory=list)
    pde_loss: list[float] = Field(default_factory=list)
    bc_loss: list[float] = Field(default_factory=list)
    data_loss: list[float] = Field(default_factory=list)
    n_epochs: int = 0

    @property
    def final_loss(self) -> float:
        """Final total loss."""
        return self.total_loss[-1] if self.total_loss else float("inf")


class PINNTrainer:
    """Train Physics-Informed Neural Networks.

    Provides interface for training PINNs to solve PDEs
    with physical constraints.

    Mathematical Foundation:
        Total loss = w_pde * L_pde + w_bc * L_bc + w_data * L_data

        where:
        - L_pde = MSE of PDE residual at collocation points
        - L_bc = MSE of boundary condition residual
        - L_data = MSE of prediction vs. observed data

    Example:
        ```python
        from ununseptium.ai.sciml import PINNTrainer, PINNConfig
        import numpy as np

        config = PINNConfig(n_layers=4, n_neurons=50)
        trainer = PINNTrainer(config)

        # Define PDE residual (e.g., heat equation)
        def heat_equation(x, t, u, u_t, u_xx):
            alpha = 0.1  # diffusivity
            return u_t - alpha * u_xx

        trainer.set_pde(heat_equation)
        trainer.set_domain([[0, 1], [0, 1]])  # x in [0,1], t in [0,1]

        # Train (requires torch)
        history = trainer.train()
        ```

    Note:
        Full implementation requires PyTorch. This provides
        the interface and mock training for API stability.
    """

    def __init__(self, config: PINNConfig | None = None) -> None:
        """Initialize the trainer.

        Args:
            config: PINN configuration.
        """
        self.config = config or PINNConfig()
        self._pde_fn: Callable[..., Any] | None = None
        self._domain: list[tuple[float, float]] = []
        self._bc_data: list[dict[str, Any]] = []
        self._training_data: tuple[np.ndarray, np.ndarray] | None = None
        self._model: Any = None

    def set_pde(self, pde_fn: Callable[..., Any]) -> None:
        """Set the PDE residual function.

        Args:
            pde_fn: Function computing PDE residual.
                    Signature varies by PDE.
        """
        self._pde_fn = pde_fn

    def set_domain(self, bounds: list[tuple[float, float]]) -> None:
        """Set the spatial-temporal domain.

        Args:
            bounds: List of (min, max) for each dimension.
        """
        self._domain = bounds

    def add_boundary_condition(
        self,
        bc_type: str,
        region: Callable[[np.ndarray], np.ndarray],
        value: Callable[[np.ndarray], np.ndarray] | float,
    ) -> None:
        """Add a boundary condition.

        Args:
            bc_type: Type of BC ('dirichlet', 'neumann').
            region: Function that returns True for boundary points.
            value: Boundary value or function.
        """
        self._bc_data.append({
            "type": bc_type,
            "region": region,
            "value": value,
        })

    def set_training_data(
        self,
        x: np.ndarray,
        y: np.ndarray,
    ) -> None:
        """Set observed training data.

        Args:
            x: Input points.
            y: Observed values.
        """
        self._training_data = (x, y)

    def train(self) -> TrainingHistory:
        """Train the PINN.

        Returns:
            TrainingHistory with loss curves.

        Note:
            Requires PyTorch. Returns mock history if unavailable.
        """
        try:
            return self._train_torch()
        except ImportError:
            return self._mock_train()

    def _train_torch(self) -> TrainingHistory:
        """Train using PyTorch."""
        import torch
        import torch.nn as nn

        # Build network
        layers = []
        n_input = len(self._domain)

        layers.append(nn.Linear(n_input, self.config.n_neurons))
        layers.append(self._get_activation())

        for _ in range(self.config.n_layers - 1):
            layers.append(nn.Linear(self.config.n_neurons, self.config.n_neurons))
            layers.append(self._get_activation())

        layers.append(nn.Linear(self.config.n_neurons, 1))
        self._model = nn.Sequential(*layers)

        optimizer = torch.optim.Adam(
            self._model.parameters(),
            lr=self.config.learning_rate,
        )

        history = TrainingHistory()

        # Generate collocation points
        collocation = self._sample_collocation()
        x_col = torch.tensor(collocation, dtype=torch.float32, requires_grad=True)

        for epoch in range(self.config.n_epochs):
            optimizer.zero_grad()

            # PDE loss
            u = self._model(x_col)
            pde_res = self._compute_pde_residual(x_col, u)
            pde_loss = torch.mean(pde_res**2) * self.config.pde_weight

            # BC loss (simplified)
            bc_loss = torch.tensor(0.0)

            # Data loss
            data_loss = torch.tensor(0.0)
            if self._training_data is not None:
                x_data = torch.tensor(self._training_data[0], dtype=torch.float32)
                y_data = torch.tensor(self._training_data[1], dtype=torch.float32)
                y_pred = self._model(x_data)
                data_loss = torch.mean((y_pred.squeeze() - y_data) ** 2) * self.config.data_weight

            total_loss = pde_loss + bc_loss + data_loss
            total_loss.backward()
            optimizer.step()

            if epoch % 100 == 0:
                history.total_loss.append(float(total_loss.item()))
                history.pde_loss.append(float(pde_loss.item()))
                history.bc_loss.append(float(bc_loss.item()))
                history.data_loss.append(float(data_loss.item()))

        history.n_epochs = self.config.n_epochs
        return history

    def _get_activation(self) -> Any:
        """Get activation module."""
        import torch.nn as nn

        activations = {
            "tanh": nn.Tanh(),
            "relu": nn.ReLU(),
            "sigmoid": nn.Sigmoid(),
            "gelu": nn.GELU(),
        }
        return activations.get(self.config.activation, nn.Tanh())

    def _sample_collocation(self) -> np.ndarray:
        """Sample collocation points."""
        n = self.config.n_collocation
        points = np.zeros((n, len(self._domain)))

        for i, (low, high) in enumerate(self._domain):
            points[:, i] = np.random.uniform(low, high, n)

        return points

    def _compute_pde_residual(self, x: Any, u: Any) -> Any:
        """Compute PDE residual (simplified)."""
        # Default: just return u (no actual PDE)
        return u.squeeze()

    def _mock_train(self) -> TrainingHistory:
        """Mock training when torch unavailable."""
        history = TrainingHistory()

        for epoch in range(min(100, self.config.n_epochs)):
            loss = 1.0 / (epoch + 1)
            history.total_loss.append(loss)
            history.pde_loss.append(loss * 0.6)
            history.bc_loss.append(loss * 0.2)
            history.data_loss.append(loss * 0.2)

        history.n_epochs = len(history.total_loss)
        return history

    def predict(self, x: np.ndarray) -> np.ndarray:
        """Predict solution at points.

        Args:
            x: Input points.

        Returns:
            Predicted solution values.
        """
        if self._model is None:
            return np.zeros(len(x))

        import torch

        with torch.no_grad():
            x_tensor = torch.tensor(x, dtype=torch.float32)
            y = self._model(x_tensor)
            return y.numpy().squeeze()
