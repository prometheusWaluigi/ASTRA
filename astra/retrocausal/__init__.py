"""
Retrocausal Extension Module (fKPZχ-R) for ASTRA

This module implements the retrocausal extension to the fKPZχ equation,
allowing for time-symmetric evolution where future states can influence past states.

The fKPZχ-R variant introduces:
1. Bidirectional time evolution
2. Quantum-like retrocausality
3. Temporal entanglement
4. Future boundary conditions
"""

from .bidirectional import (
    evolve_bidirectional,
    retrocausal_step,
    temporal_entanglement,
    compute_temporal_correlation
)

from .boundary import (
    FutureBoundaryCondition,
    set_future_boundary,
    apply_boundary_constraint
)

__all__ = [
    'evolve_bidirectional',
    'retrocausal_step',
    'temporal_entanglement',
    'compute_temporal_correlation',
    'FutureBoundaryCondition',
    'set_future_boundary',
    'apply_boundary_constraint'
]
