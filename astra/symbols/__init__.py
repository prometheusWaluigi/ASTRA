"""
Symbolic Narrative Layer (𝓂-Layer) for ASTRA

This module provides the symbolic interpretation layer for ASTRA,
translating topological patterns in the qualia field into meaningful
archetypal narratives.

The 𝓂-Layer sits on top of the χ-Layer (field) and 𝓈-Layer (topology),
providing a symbolic interface to the underlying mathematical structures.
"""

from .narrative import (
    generate_narrative,
    interpret_motifs,
    create_event_log,
    NarrativeEvent,
    EventType
)

from .threshold import (
    detect_threshold_crossings,
    ThresholdType,
    ThresholdEvent
)

__all__ = [
    'generate_narrative',
    'interpret_motifs',
    'create_event_log',
    'NarrativeEvent',
    'EventType',
    'detect_threshold_crossings',
    'ThresholdType',
    'ThresholdEvent'
]
