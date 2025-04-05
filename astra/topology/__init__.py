"""
ASTRA Topology Module - 𝓈-Layer Implementation

This module implements the topological analysis layer (𝓈-Layer) of the ASTRA architecture.
It provides tools for analyzing the topological structure of the qualia field using
persistent homology, Betti numbers, and other TDA techniques.
"""

from .persistence import (
    compute_persistence_diagram,
    compute_betti_numbers,
    plot_persistence_diagram,
    persistence_landscape
)

from .ricci import (
    compute_ollivier_ricci_curvature,
    compute_forman_ricci_curvature,
    plot_ricci_curvature
)

from .motifs import (
    detect_topological_motifs,
    classify_attractor_type,
    plot_attractor_landscape
)

__all__ = [
    # Persistence homology
    'compute_persistence_diagram',
    'compute_betti_numbers',
    'plot_persistence_diagram',
    'persistence_landscape',
    
    # Ricci curvature
    'compute_ollivier_ricci_curvature',
    'compute_forman_ricci_curvature',
    'plot_ricci_curvature',
    
    # Topological motifs
    'detect_topological_motifs',
    'classify_attractor_type',
    'plot_attractor_landscape'
]
