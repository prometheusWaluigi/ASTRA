"""
ASTRA Core Module - χ-Layer Implementation

This module contains the foundational components for the ASTRA system:
- QualiaField: The central data structure representing the χ(x,t) qualia field
- Evolution functions: The fKPZχ equation implementation that evolves the field

These components implement the χ-Layer from the ASTRA architecture, which
is the concrete implementation of the Quantum-State Modeling described in 
the PRD.
"""

from .field import QualiaField
from .evolution import (
    fractional_laplacian_fft,
    evolve_step,
    evolve_chart,
    visualize_evolution
)

# Default export - interfaces mentioned in README
__all__ = [
    'QualiaField',        # Field class
    'evolve_chart',       # Main evolution function 
    'fractional_laplacian_fft',  # Core mathematical implementation
]
