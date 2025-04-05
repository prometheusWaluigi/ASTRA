"""
Narrative Generation Module for ASTRA

This module translates topological patterns in the qualia field into
symbolic narratives based on archetypal patterns.

It provides tools for:
- Interpreting topological motifs as archetypal patterns
- Generating narrative descriptions of field states
- Creating event logs of significant transitions
"""

import numpy as np
from typing import Dict, List, Tuple, Any, Optional, Union, Callable
from enum import Enum, auto
from datetime import datetime
import json

# Flag for topology module availability
TOPOLOGY_AVAILABLE = False

# Only import topology components when needed
def _load_topology():
    global TOPOLOGY_AVAILABLE
    try:
        from ..topology.motifs import detect_topological_motifs, classify_attractor_type
        from ..topology.persistence import compute_persistence_diagram, compute_betti_numbers
        from ..topology.ricci import compute_joy_field
        TOPOLOGY_AVAILABLE = True
        return detect_topological_motifs, classify_attractor_type, compute_persistence_diagram, compute_betti_numbers, compute_joy_field
    except ImportError:
        import warnings
        warnings.warn("Topology module not available. Narrative generation will use simplified methods.")
        return None, None, None, None, None


class EventType(Enum):
    """Types of narrative events that can occur in the qualia field."""
    EMERGENCE = auto()       # New structure emerges
    DISSOLUTION = auto()     # Structure dissolves
    TRANSFORMATION = auto()  # Structure transforms
    INTEGRATION = auto()     # Structures integrate
    BIFURCATION = auto()     # Structure splits
    RESONANCE = auto()       # Structures resonate
    THRESHOLD = auto()       # Threshold crossing
    TRANSIT = auto()         # Planetary transit effect
    ASPECT = auto()          # Aspect formation
    MEDITATION = auto()      # Meditation effect
    INSIGHT = auto()         # Insight formation
    CATHARSIS = auto()       # Emotional release
    RECURSIVE_LOOP = auto()   # Field enters a cyclical pattern
    STRANGE_ATTRACTOR = auto() # Complex dynamics, creative potential
    
    # Jungian Archetypes
    THE_HERO = auto()          # Represents courage and transformation
    THE_MENTOR = auto()        # Guidance and wisdom
    THE_SHADOW = auto()        # Repressed aspects of the self
    THE_TRICKSTER = auto()     # Chaos and disruption
    THE_LOVER = auto()         # Passion and connection
    THE_WARRIOR = auto()       # Strength and protection
    THE_SEEKER = auto()        # Exploration and discovery
    THE_RULER = auto()         # Order and control
    THE_INNOCENT = auto()      # Faith and optimism
    THE_ORPHAN = auto()        # Empathy and connection to suffering

    # Hero's Journey Stages
    CALL_TO_ADVENTURE = auto()
    MEETING_THE_MENTOR = auto()
    CROSSING_THE_THRESHOLD = auto()
    TESTS_ALLIES_ENEMIES = auto()
    APPROACH_TO_THE_INMOST_CAVE = auto()
    THE_ORDEAL = auto()
    REWARD = auto()
    THE_ROAD_BACK = auto()
    THE_RESURRECTION = auto()
    RETURN_WITH_THE_ELIXIR = auto()


class NarrativeEvent:
    """
    Represents a significant event in the qualia field narrative.
    
    Attributes:
        timestamp: When the event occurred (simulation time)
        event_type: Type of event
        description: Human-readable description
        intensity: Intensity of the event (0.0-1.0)
        location: Coordinates in the field where event occurred
        betti_numbers: Topological features at time of event
        joy_value: Joy (negative curvature) at time of event
        metadata: Additional event-specific data
    """
    
    def __init__(self, 
                 timestamp: float,
                 event_type: EventType,
                 description: str,
                 intensity: float = 0.5,
                 location: Optional[Tuple[int, int]] = None,
                 betti_numbers: Optional[List[int]] = None,
                 joy_value: Optional[float] = None,
                 metadata: Optional[Dict[str, Any]] = None):
        """Initialize a narrative event."""
        self.timestamp = timestamp
        self.event_type = event_type
        self.description = description
        self.intensity = max(0.0, min(1.0, intensity))  # Clamp to [0,1]
        self.location = location
        self.betti_numbers = betti_numbers
        self.joy_value = joy_value
        self.metadata = metadata or {}
        self.real_time = datetime.now()  # When this event was created
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary for serialization."""
        # Helper function to convert individual values to JSON-serializable format
        def convert_to_serializable(v):
            # Handle Enum values
            if isinstance(v, Enum):
                return v.name
            # Handle numpy values
            elif isinstance(v, np.integer):
                return int(v)
            elif isinstance(v, np.floating):
                return float(v)
            elif isinstance(v, np.ndarray):
                return v.tolist()
            # Handle datetime objects
            elif isinstance(v, datetime):
                return v.isoformat()
            # Handle objects with to_dict method
            elif hasattr(v, 'to_dict'):
                return v.to_dict()
            # Handle sequences (lists, tuples)
            elif isinstance(v, (list, tuple)):
                return [convert_to_serializable(item) for item in v]
            # Use simple types directly
            elif isinstance(v, (str, int, float, bool, type(None))):
                return v
            # Convert other types to strings
            else:
                return str(v)
        
        # Create a JSON-safe metadata dictionary
        safe_metadata = {}
        if self.metadata:
            for k, v in self.metadata.items():
                safe_metadata[k] = convert_to_serializable(v)
        
        # Convert betti_numbers if present
        safe_betti = None
        if self.betti_numbers is not None:
            safe_betti = convert_to_serializable(self.betti_numbers)
        
        # Convert joy_value if present
        safe_joy = None
        if self.joy_value is not None:
            safe_joy = convert_to_serializable(self.joy_value)
        
        # Convert location if present
        safe_location = None
        if self.location is not None:
            safe_location = convert_to_serializable(self.location)
        
        return {
            'timestamp': float(self.timestamp),
            'event_type': self.event_type.name,
            'description': self.description,
            'intensity': float(self.intensity),
            'location': safe_location,
            'betti_numbers': safe_betti,
            'joy_value': safe_joy,
            'metadata': safe_metadata,
            'real_time': self.real_time.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'NarrativeEvent':
        """Create event from dictionary."""
        event = cls(
            timestamp=data['timestamp'],
            event_type=EventType[data['event_type']],
            description=data['description'],
            intensity=data['intensity'],
            location=data['location'],
            betti_numbers=data['betti_numbers'],
            joy_value=data['joy_value'],
            metadata=data['metadata']
        )
        event.real_time = datetime.fromisoformat(data['real_time'])
        return event
    
    def __str__(self) -> str:
        """String representation of the event."""
        return f"[{self.timestamp:.2f}] {self.event_type.name}: {self.description} (Intensity: {self.intensity:.2f})"


# Archetypal pattern descriptions
ARCHETYPAL_PATTERNS = {
    'RECURSIVE_LOOP': {
        'name': 'Recursive Loop',
        'description': 'A self-referential thought pattern creating a feedback loop',
        'psychological_state': 'Introspection, self-reflection, recursive thinking',
        'narrative_templates': [
            "A recursive pattern emerges, creating a self-referential loop in consciousness",
            "Thoughts begin to circle back on themselves, creating a recursive structure",
            "A self-reflective loop forms, allowing consciousness to observe itself",
            "The mind turns inward, creating a recursive pattern of self-observation"
        ]
    },
    'EGO_CONDENSATION': {
        'name': 'Ego Condensation',
        'description': 'Crystallization of identity structures',
        'psychological_state': 'Identity formation, ego strengthening, boundary creation',
        'narrative_templates': [
            "The ego structure crystallizes, creating a stronger sense of self",
            "Identity boundaries form and solidify, creating a distinct sense of 'I'",
            "A condensation of self-concept occurs, strengthening ego structures",
            "The field condenses around a central identity, reinforcing ego boundaries"
        ]
    },
    'DISSOLUTION': {
        'name': 'Dissolution',
        'description': 'Boundary dissolution, ego death',
        'psychological_state': 'Transcendence, mystical experience, ego death',
        'narrative_templates': [
            "Boundaries begin to dissolve, creating a sense of unity with the field",
            "Ego structures temporarily dissolve, allowing for transcendent experience",
            "A dissolution of identity boundaries occurs, opening to larger consciousness",
            "The field enters a dissolution phase, where rigid structures break down"
        ]
    },
    'INTEGRATION': {
        'name': 'Integration',
        'description': 'Integration of disparate elements',
        'psychological_state': 'Wholeness, synthesis, resolution of conflicts',
        'narrative_templates': [
            "Previously separate elements integrate into a coherent whole",
            "A synthesis occurs, bringing together disparate aspects of consciousness",
            "An integration process begins, harmonizing conflicting elements",
            "The field reorganizes toward greater coherence and integration"
        ]
    },
    'CATHARSIS': {
        'name': 'Catharsis',
        'description': 'Emotional release pattern',
        'psychological_state': 'Release, emotional clearing, breakthrough',
        'narrative_templates': [
            "An emotional release occurs, clearing blocked energy in the field",
            "A cathartic pattern emerges, allowing for emotional processing",
            "Tension in the field releases in a cathartic breakthrough",
            "A sudden release of built-up potential creates a cathartic shift"
        ]
    },
    'INSIGHT': {
        'name': 'Insight Formation',
        'description': 'Sudden understanding or realization',
        'psychological_state': 'Clarity, understanding, breakthrough',
        'narrative_templates': [
            "A sudden insight emerges, creating new connections in the field",
            "A moment of clarity occurs, reorganizing the field structure",
            "An insight forms, bringing previously unrelated elements together",
            "A breakthrough in understanding creates a new pattern in the field"
        ]
    },
    'BIFURCATION': {
        'name': 'Bifurcation',
        'description': 'Splitting of consciousness into parallel streams',
        'psychological_state': 'Choice point, divergent thinking, parallel processing',
        'narrative_templates': [
            "The field bifurcates, creating parallel streams of consciousness",
            "A choice point emerges, splitting the field into potential futures",
            "A bifurcation occurs, allowing multiple perspectives to coexist",
            "The unified field splits into distinct streams, creating a decision point"
        ]
    }
}


def interpret_motifs(motifs: Union[Dict[str, Any], np.ndarray], 
                    joy_field: Optional[np.ndarray] = None,
                    timestamp: float = 0.0) -> List[NarrativeEvent]:
    """
    Interpret detected topological motifs as archetypal patterns.
    
    Args:
        motifs: Dictionary of detected motifs from topology module or numpy array
        joy_field: Optional joy field (negative curvature)
        timestamp: Current simulation time
        
    Returns:
        List of narrative events corresponding to the motifs
    """
    events = []
    
    # Handle numpy array case (basic stats about the field)
    if isinstance(motifs, np.ndarray):
        mean_val = np.mean(motifs)
        max_val = np.max(motifs)
        min_val = np.min(motifs)
        std_val = np.std(motifs)
        
        # High variability in the field
        if std_val > 0.2 * (max_val - min_val) and max_val > min_val:
            event = NarrativeEvent(
                timestamp=timestamp,
                event_type=EventType.CATHARSIS,
                description="Field exhibits high variability, suggesting emotional processing",
                intensity=min(1.0, std_val / (max_val - min_val))
            )
            events.append(event)
        
        return events
    
    # Dictionary case - process each detected motif
    for motif_type, motif_data in motifs.items():
        if motif_type == 'attractor':
            for attractor in motif_data:
                # Existing attractor logic
                event = NarrativeEvent(
                    timestamp=timestamp,
                    event_type=EventType.EMERGENCE,
                    description=f"An attractor of type {attractor['type']} emerges at {attractor['location']}",
                    intensity=attractor['persistence'],
                    location=attractor['location'],
                    joy_value=np.mean(joy_field) if joy_field is not None else None
                )
                events.append(event)

                # Check for Hero archetype
                if attractor['persistence'] > 0.7 and attractor['size'] > 10:
                    hero_event = NarrativeEvent(
                        timestamp=timestamp,
                        event_type=EventType.THE_HERO,
                        description="A strong attractor emerges, representing the Hero archetype",
                        intensity=attractor['persistence'],
                        location=attractor['location'],
                        joy_value=np.mean(joy_field) if joy_field is not None else None
                    )
                    events.append(hero_event)
                    
                # Check for Mentor archetype
                for event in events:
                    if event.event_type == EventType.THE_HERO and \
                       np.linalg.norm(np.array(attractor['location']) - np.array(event.location)) < 5 and \
                       attractor['persistence'] > 0.5 and attractor['size'] > 5 and attractor['size'] < 10:
                        mentor_event = NarrativeEvent(
                            timestamp=timestamp,
                            event_type=EventType.THE_MENTOR,
                            description="A stable attractor appears near the Hero, representing the Mentor archetype",
                            intensity=attractor['persistence'],
                            location=attractor['location'],
                            joy_value=np.mean(joy_field) if joy_field is not None else None
                        )
                        events.append(mentor_event)
        elif motif_type in ARCHETYPAL_PATTERNS:
            pattern = ARCHETYPAL_PATTERNS[motif_type]
            
            # Select a narrative template
            import random
            template = random.choice(pattern['narrative_templates'])
            
            # Calculate intensity based on confidence and prominence
            intensity = motif_data.get('confidence', 0.5) * motif_data.get('prominence', 1.0)
            
            # Create event
            event = NarrativeEvent(
                timestamp=timestamp,
                event_type=EventType.EMERGENCE,  # Default to emergence
                description=template,
                intensity=intensity,
                location=motif_data.get('location'),
                betti_numbers=motif_data.get('betti'),
                joy_value=motif_data.get('joy_value'),
                metadata={
                    'pattern_name': pattern['name'],
                    'psychological_state': pattern['psychological_state'],
                    'stability': motif_data.get('stability', 'medium')
                }
            )
            
            events.append(event)
    
    return events


def generate_narrative(field: np.ndarray, 
                      prev_field: Optional[np.ndarray] = None,
                      timestamp: float = 0.0,
                      detect_motifs: bool = True) -> List[NarrativeEvent]:
    """
    Generate narrative events from the current field state.
    
    Args:
        field: Current qualia field state
        prev_field: Previous field state (for detecting changes)
        timestamp: Current simulation time
        detect_motifs: Whether to detect topological motifs
        
    Returns:
        List of narrative events
    """
    events = []
    
    # Use basic field statistics to generate narratives
    mean_val = np.mean(field)
    max_val = np.max(field)
    min_val = np.min(field)
    std_val = np.std(field)
    
    # Detect high variability (potential catharsis)
    if std_val > 0.2 * (max_val - min_val):
        event = NarrativeEvent(
            timestamp=timestamp,
            event_type=EventType.CATHARSIS,
            description="High variability in the field suggests emotional processing",
            intensity=min(1.0, std_val / (max_val - min_val))
        )
        events.append(event)
    
    # Detect high average (potential integration)
    if mean_val > 0.7 * max_val:
        event = NarrativeEvent(
            timestamp=timestamp,
            event_type=EventType.INTEGRATION,
            description="Elevated field values suggest integration of consciousness",
            intensity=mean_val / max_val
        )
        events.append(event)
    
    # Only attempt topology-based analysis if requested
    if detect_motifs:
        detect_fn, classify_fn, persistence_fn, betti_fn, joy_fn = _load_topology()
        if all([detect_fn, classify_fn, persistence_fn, betti_fn, joy_fn]):
            # Full narrative generation with topology module
            # Compute persistence diagram
            persistence = persistence_fn(field)
            betti = betti_fn(persistence['diagrams'])
            
            # Compute joy field
            joy = joy_fn(field)
            
            # Detect topological motifs
            motifs = detect_fn(field)
            motif_events = interpret_motifs(motifs, joy, timestamp)
            events.extend(motif_events)
            
            # Detect attractor type
            attractor = classify_fn(field)
            
            # Generate event based on attractor type
            if attractor['attractor_type'] == 'fixed_point':
                event = NarrativeEvent(
                    timestamp=timestamp,
                    event_type=EventType.INTEGRATION,
                    description="The field stabilizes around a fixed point, suggesting integration",
                    intensity=attractor['confidence'],
                    betti_numbers=betti,
                    joy_value=np.mean(joy),
                    metadata={'attractor_type': attractor['attractor_type']}
                )
                events.append(event)
            
            elif attractor['attractor_type'] == 'limit_cycle':
                event = NarrativeEvent(
                    timestamp=timestamp,
                    event_type=EventType.RECURSIVE_LOOP,
                    description="The field enters a cyclical pattern, suggesting recursive thought",
                    intensity=attractor['confidence'],
                    betti_numbers=betti,
                    joy_value=np.mean(joy),
                    metadata={'attractor_type': attractor['attractor_type']}
                )
                events.append(event)
            
            elif attractor['attractor_type'] == 'strange_attractor':
                event = NarrativeEvent(
                    timestamp=timestamp,
                    event_type=EventType.BIFURCATION,
                    description="The field exhibits complex dynamics, suggesting creative potential",
                    intensity=attractor['confidence'],
                    betti_numbers=betti,
                    joy_value=np.mean(joy),
                    metadata={'attractor_type': attractor['attractor_type']}
                )
                events.append(event)
    
    # Detect changes if previous field is provided
    if prev_field is not None:
        # Calculate field difference
        diff = field - prev_field
        max_change = np.max(np.abs(diff))
        
        # Detect significant changes
        if max_change > 0.3 * np.max(field):
            # Determine if change is increase or decrease
            if np.sum(diff > 0) > np.sum(diff < 0):
                event = NarrativeEvent(
                    timestamp=timestamp,
                    event_type=EventType.EMERGENCE,
                    description="A significant increase in field intensity suggests emergence",
                    intensity=min(1.0, max_change / np.max(field))
                )
                events.append(event)
            else:
                event = NarrativeEvent(
                    timestamp=timestamp,
                    event_type=EventType.DISSOLUTION,
                    description="A significant decrease in field intensity suggests dissolution",
                    intensity=min(1.0, max_change / np.max(field))
                )
                events.append(event)
    
    return events


def create_event_log(events: List[NarrativeEvent], 
                    output_file: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a structured event log from narrative events.
    
    Args:
        events: List of narrative events
        output_file: Optional file to save the event log
        
    Returns:
        Dictionary with event log data
    """
    # Sort events by timestamp
    sorted_events = sorted(events, key=lambda e: e.timestamp)
    
    # Create event log structure
    event_log = {
        'version': '0.1',
        'generated_at': datetime.now().isoformat(),
        'event_count': len(sorted_events),
        'time_range': {
            'start': sorted_events[0].timestamp if sorted_events else 0,
            'end': sorted_events[-1].timestamp if sorted_events else 0
        },
        'events': [event.to_dict() for event in sorted_events]
    }
    
    # Save to file if requested
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(event_log, f, indent=2)
    
    return event_log
