"""Scientific ML submodule.

Provides PINN, Neural Operator, and Neural ODE interfaces.
"""

from ununseptium.ai.sciml.constraints import PhysicsConstraint, SoftConstraint
from ununseptium.ai.sciml.neural_ode import NeuralODEConfig, NeuralODESolver
from ununseptium.ai.sciml.neural_operator import FNOConfig, NeuralOperator
from ununseptium.ai.sciml.pinn import PINNConfig, PINNTrainer

__all__ = [
    # Neural Operator
    "FNOConfig",
    # Neural ODE
    "NeuralODEConfig",
    "NeuralODESolver",
    "NeuralOperator",
    # PINN
    "PINNConfig",
    "PINNTrainer",
    # Constraints
    "PhysicsConstraint",
    "SoftConstraint",
]
