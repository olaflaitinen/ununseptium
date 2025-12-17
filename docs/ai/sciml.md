# Scientific ML

## Scope

This document describes Scientific ML methods in ununseptium, including Physics-Informed Neural Networks (PINNs) and Neural ODEs.

### Non-Goals

- Full SciML framework
- PDE solvers
- Surrogate modeling platform

## Definitions

| Term | Definition |
|------|------------|
| PINN | Physics-Informed Neural Network |
| Neural ODE | Neural network defining ODE dynamics |
| Physics Loss | Penalty for violating physical constraints |

See [Glossary](../glossary.md) for additional terminology.

## Physics-Informed Neural Networks

### Concept

PINNs incorporate domain knowledge as constraints:

```mermaid
graph TB
    DATA[Training Data] --> NN[Neural Network]
    PHYSICS[Physics Constraints] --> LOSS[Loss Function]
    NN --> PRED[Predictions]
    PRED --> DATA_LOSS[Data Loss]
    PRED --> LOSS
    DATA_LOSS --> TOTAL[Total Loss]
    LOSS --> TOTAL

```text
### Total Loss

$$\mathcal{L} = \mathcal{L}_{data} + \lambda \mathcal{L}_{physics}$$

Where:
- $\mathcal{L}_{data}$ is standard prediction loss
- $\mathcal{L}_{physics}$ is constraint violation
- $\lambda$ balances data fit vs. physics

### Interface

```python
from ununseptium.ai.sciml import PINN

class RiskDynamics(PINN):
    def physics_loss(self, x, y):
        # Risk must be non-negative
        return torch.relu(-y).mean()

    def domain_constraints(self, x, y):
        # Sum of probabilities = 1
        return (y.sum(dim=-1) - 1).pow(2).mean()

model = RiskDynamics(hidden_layers=[64, 64])
model.fit(X_train, y_train, physics_weight=0.1)

```text
### Use Cases

| Application | Physics Constraint |
|-------------|-------------------|
| Risk scores | Non-negativity |
| Probabilities | Sum to 1 |
| Time series | Monotonicity |
| Conservation | Balance equations |

## Neural ODEs

### Concept

Model continuous dynamics:

$$\frac{dy}{dt} = f_\theta(y, t)$$

Solution via ODE solver:

$$y(T) = y(0) + \int_0^T f_\theta(y(t), t) dt$$

### Interface

```python
from ununseptium.ai.sciml import NeuralODE

model = NeuralODE(
    input_dim=10,
    hidden_dim=64,
    method="dopri5",  # ODE solver
)

# Predict at any time point
y_t = model.forward(y0, t)

```text
### Training

```python
# Train on trajectories
model.fit(trajectories, times)

# Predict trajectory
trajectory = model.predict(y0, t_grid)

```text
### ODE Solvers

| Solver | Accuracy | Speed |
|--------|----------|-------|
| `euler` | Low | Fast |
| `rk4` | Medium | Medium |
| `dopri5` | High | Slow |
| `adaptive` | High | Variable |

## Application: Risk Dynamics

### Time-Varying Risk

```python
from ununseptium.ai.sciml import NeuralODE

# Model risk evolution
risk_dynamics = NeuralODE(input_dim=1, hidden_dim=32)
risk_dynamics.fit(historical_risk, times)

# Predict future risk
future_risk = risk_dynamics.predict(current_risk, future_times)

```text
### Constrained Risk Model

```python
class ConstrainedRiskModel(PINN):
    def physics_loss(self, features, risk):
        losses = []

        # Risk bounds [0, 1]
        losses.append(torch.relu(-risk).mean())
        losses.append(torch.relu(risk - 1).mean())

        # Monotonicity in certain features
        # Higher transaction count -> higher risk
        grad = torch.autograd.grad(risk, features, create_graph=True)
        losses.append(torch.relu(-grad[..., 0]).mean())

        return sum(losses)

```text
## Hybrid Models

Combine data-driven and physics:

```python
from ununseptium.ai.sciml import HybridModel

class HybridRisk(HybridModel):
    def __init__(self):
        self.nn = NeuralNetwork(...)
        self.physics = PhysicsModel(...)

    def forward(self, x):
        nn_pred = self.nn(x)
        physics_pred = self.physics(x)
        return 0.7 * nn_pred + 0.3 * physics_pred

```text
## Performance

| Model | Training | Inference |
|-------|----------|-----------|
| PINN | Slow (physics evals) | Fast |
| Neural ODE | Slow (ODE solves) | Medium |
| Hybrid | Medium | Fast |

## Dependencies

SciML features require PyTorch:

```bash
pip install ununseptium[ai-torch]

```text
Optional for advanced solvers:

```bash
pip install torchdiffeq  # Neural ODE solvers

```text
## Related Documentation

- [AI Overview](ai-overview.md)
- [Governance](governance.md)
- [AI Pipeline](../architecture/ai-pipeline.md)

## References

- Raissi, M., Perdikaris, P., & Karniadakis, G. E. (2019). Physics-informed neural networks.
- Chen, R. T. Q., et al. (2018). Neural Ordinary Differential Equations.
- [Glossary](../glossary.md)
