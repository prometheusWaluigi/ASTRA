"""
Simplified test script for the ASTRA symbolic narrative layer (𝓂-Layer).

This script demonstrates the basic narrative generation capabilities of ASTRA
without relying on the full topology module.
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import json
import traceback
from datetime import datetime

# Create output directory if it doesn't exist
os.makedirs("output", exist_ok=True)

print("Testing ASTRA symbolic narrative layer (𝓂-Layer) with simplified approach...")

try:
    # Import ASTRA components
    from astra.core.field import QualiaField
    from astra.core.evolution import evolve_chart
    from astra.symbols.narrative import NarrativeEvent, EventType
    from astra.symbols.threshold import ThresholdType, ThresholdEvent
    
    # Create a mock natal data object (similar structure to Kerykeion's AstrologicalSubject)
    class MockNatalData:
        def __init__(self):
            self.name = "Jan 4, 1985 - Minneapolis"
            
            # Mock planets with positions (based on the Jan 4, 1985, 5am, Minneapolis chart)
            self.sun = {'abs_pos': 283.89, 'pos': 13.89, 'sign': 'Cap', 'emoji': '♑️', 'house': '1st House', 'retrograde': False}
            self.moon = {'abs_pos': 342.00, 'pos': 12.00, 'sign': 'Pis', 'emoji': '♓️', 'house': '2nd House', 'retrograde': False}
            self.mercury = {'abs_pos': 270.18, 'pos': 0.18, 'sign': 'Cap', 'emoji': '♑️', 'house': '1st House', 'retrograde': False}
            self.venus = {'abs_pos': 264.33, 'pos': 24.33, 'sign': 'Sag', 'emoji': '♐️', 'house': '12th House', 'retrograde': False}
            self.mars = {'abs_pos': 347.56, 'pos': 17.56, 'sign': 'Pis', 'emoji': '♓️', 'house': '3rd House', 'retrograde': False}
            self.jupiter = {'abs_pos': 270.26, 'pos': 0.26, 'sign': 'Cap', 'emoji': '♑️', 'house': '1st House', 'retrograde': False}
            self.saturn = {'abs_pos': 233.69, 'pos': 23.69, 'sign': 'Sco', 'emoji': '♏️', 'house': '11th House', 'retrograde': True}
            self.uranus = {'abs_pos': 255.64, 'pos': 15.64, 'sign': 'Sag', 'emoji': '♐️', 'house': '12th House', 'retrograde': False}
            self.neptune = {'abs_pos': 272.05, 'pos': 2.05, 'sign': 'Cap', 'emoji': '♑️', 'house': '1st House', 'retrograde': False}
            self.pluto = {'abs_pos': 214.40, 'pos': 4.40, 'sign': 'Sco', 'emoji': '♏️', 'house': '11th House', 'retrograde': True}
            
            # Mock houses
            self.first_house = {'abs_pos': 278.19, 'pos': 8.19, 'sign': 'Cap', 'emoji': '♑️'}
            
            # These are the planets that will be accessed
            self.planets = [
                self.sun, self.moon, self.mercury, self.venus, self.mars,
                self.jupiter, self.saturn, self.uranus, self.neptune, self.pluto
            ]
    
    # Create mock natal data
    mock_natal = MockNatalData()
    print("✓ Created mock natal data")
    
    # Initialize QualiaField with smaller grid for faster testing
    print("\nInitializing QualiaField...")
    field = QualiaField(mock_natal, grid_size=(64, 64))
    print("✓ QualiaField initialized")
    
    # Evolve the field over time
    print("\nEvolving field over time...")
    duration = 2.0  # Simulate 2 time units
    dt = 0.1        # Time step
    store_frames = 10  # Store 10 frames for analysis
    
    # evolve_chart returns a tuple of (field_history, time_points)
    field_history, timestamps = evolve_chart(field, duration=duration, dt=dt, store_frames=store_frames)
    
    print(f"✓ Field evolved over {len(timestamps)} time steps from t={timestamps[0]} to t={timestamps[-1]}")
    
    # Simplified narrative generation
    print("\nGenerating simplified symbolic narratives...")
    all_events = []
    
    # Define archetypal patterns
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
        }
    }
    
    # Generate simplified narratives for each time step
    for i in range(1, len(field_history)):
        current_field = field_history[i]
        prev_field = field_history[i-1]
        timestamp = timestamps[i]
        
        # Calculate basic field statistics
        mean_val = np.mean(current_field)
        max_val = np.max(current_field)
        min_val = np.min(current_field)
        std_val = np.std(current_field)
        
        # Calculate field difference
        diff = current_field - prev_field
        mean_change = np.mean(np.abs(diff))
        max_change = np.max(np.abs(diff))
        
        # Generate events based on simple heuristics
        events_for_timestep = []
        
        # 1. Check for high variability (potential catharsis)
        if std_val > 0.2 * (max_val - min_val) and max_val > min_val:
            intensity = min(1.0, std_val / (max_val - min_val))
            events_for_timestep.append(
                NarrativeEvent(
                    timestamp=timestamp,
                    event_type=EventType.CATHARSIS,
                    description="High variability in the field suggests emotional processing",
                    intensity=intensity
                )
            )
        
        # 2. Check for high average (potential integration)
        if mean_val > 0.7 * max_val:
            intensity = min(1.0, mean_val / max_val)
            events_for_timestep.append(
                NarrativeEvent(
                    timestamp=timestamp,
                    event_type=EventType.INTEGRATION,
                    description="Elevated field values suggest integration of consciousness",
                    intensity=intensity
                )
            )
        
        # 3. Check for significant changes (emergence or dissolution)
        if max_change > 0.2 * np.max(current_field):
            # Determine if change is increase or decrease
            if np.sum(diff > 0) > np.sum(diff < 0):
                event_type = EventType.EMERGENCE
                description = "A significant increase in field intensity suggests emergence"
            else:
                event_type = EventType.DISSOLUTION
                description = "A significant decrease in field intensity suggests dissolution"
            
            intensity = min(1.0, max_change / np.max(current_field))
            events_for_timestep.append(
                NarrativeEvent(
                    timestamp=timestamp,
                    event_type=event_type,
                    description=description,
                    intensity=intensity
                )
            )
        
        # 4. Detect threshold crossings
        # Find local maxima as potential insight points
        from scipy.ndimage import maximum_filter
        max_filtered = maximum_filter(current_field, size=3)
        maxima = (current_field == max_filtered) & (current_field > 0.8 * max_val)
        
        if np.any(maxima):
            # Get coordinates of highest maximum
            max_coords = np.unravel_index(np.argmax(current_field * maxima), current_field.shape)
            
            # Create threshold event
            threshold_event = ThresholdEvent(
                timestamp=timestamp,
                threshold_type=ThresholdType.VALUE,
                threshold_value=0.8 * max_val,
                field_value=current_field[max_coords],
                description="A peak in the field suggests an insight or realization",
                location=max_coords
            )
            
            # Convert to narrative event
            narrative_event = threshold_event.to_narrative_event()
            # Convert numpy location to regular tuple if it exists
            if narrative_event.location is not None:
                narrative_event.location = tuple(map(int, narrative_event.location))
            events_for_timestep.append(narrative_event)
        
        # 5. Randomly select an archetypal pattern for this timestep
        if i % 3 == 0:  # Every third timestep
            import random
            pattern_key = random.choice(list(ARCHETYPAL_PATTERNS.keys()))
            pattern = ARCHETYPAL_PATTERNS[pattern_key]
            
            # Select a narrative template
            template = random.choice(pattern['narrative_templates'])
            
            # Calculate intensity based on field statistics
            intensity = random.uniform(0.5, 0.9)
            
            # Create event
            events_for_timestep.append(
                NarrativeEvent(
                    timestamp=timestamp,
                    event_type=EventType.EMERGENCE,
                    description=template,
                    intensity=intensity,
                    metadata={
                        'pattern_name': pattern['name'],
                        'psychological_state': pattern['psychological_state']
                    }
                )
            )
        
        # Add events for this timestep to overall list
        all_events.extend(events_for_timestep)
        print(f"  Time {timestamp:.2f}: Generated {len(events_for_timestep)} events")
    
    # Create event log
    print("\nCreating event log...")
    
    # Sort events by timestamp
    sorted_events = sorted(all_events, key=lambda e: e.timestamp)
    
    # Create event log structure
    event_log = {
        'version': '0.1',
        'generated_at': datetime.now().isoformat(),
        'event_count': len(sorted_events),
        'time_range': {
            'start': float(sorted_events[0].timestamp) if sorted_events else 0,
            'end': float(sorted_events[-1].timestamp) if sorted_events else 0
        },
        'events': [event.to_dict() for event in sorted_events]
    }
    
    # Define a custom JSON encoder to handle numpy types
    class NumpyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, datetime):
                return obj.isoformat()
            elif isinstance(obj, bool):
                return bool(obj)  # Handle boolean values
            elif obj is None:
                return None
            elif hasattr(obj, 'to_dict'):
                return obj.to_dict()  # Handle custom objects with to_dict method
            return super(NumpyEncoder, self).default(obj)
    
    # Save to file
    import json
    with open("output/narrative_events.json", 'w') as f:
        json.dump(event_log, f, indent=2, cls=NumpyEncoder)
    
    print(f"✓ Created event log with {len(all_events)} events")
    
    # Display some sample events
    print("\nSample narrative events:")
    for i, event in enumerate(sorted_events[:5]):
        print(f"  {i+1}. {event}")
    
    # Create visualization of field evolution with events
    print("\nCreating visualization...")
    
    # Select key frames for visualization
    key_frames = [0, len(field_history)//3, 2*len(field_history)//3, -1]
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()
    
    for i, frame_idx in enumerate(key_frames):
        ax = axes[i]
        frame = field_history[frame_idx]
        time = timestamps[frame_idx]
        
        # Plot the field
        im = ax.imshow(frame, cmap='viridis', origin='lower')
        plt.colorbar(im, ax=ax)
        
        # Find events near this time
        nearby_events = [e for e in all_events if abs(e.timestamp - time) < dt]
        
        # Add title with time and event count
        ax.set_title(f"t={time:.2f} ({len(nearby_events)} events)")
        
        # Add event markers if they have locations
        for event in nearby_events:
            if event.location and isinstance(event.location, (list, tuple)) and len(event.location) == 2:
                try:
                    y, x = event.location
                    ax.plot(x, y, 'ro', markersize=10, alpha=0.7)
                    
                    # Add event type as text
                    ax.text(x+2, y+2, event.event_type.name[:4], color='white', 
                           fontsize=8, bbox=dict(facecolor='red', alpha=0.5))
                except (ValueError, TypeError):
                    # Skip if location is not properly formatted
                    pass
    
    plt.suptitle(f"Qualia Field Evolution with Narrative Events\n{mock_natal.name}", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    # Save the figure
    output_file = os.path.join("output", "narrative_visualization.png")
    plt.savefig(output_file)
    plt.close(fig)
    print(f"✓ Saved visualization to {output_file}")
    
    # Create event timeline visualization
    print("\nCreating event timeline...")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Group events by type
    event_types = {}
    for event in all_events:
        if event.event_type.name not in event_types:
            event_types[event.event_type.name] = []
        event_types[event.event_type.name].append(event)
    
    # Plot events on timeline
    colors = plt.cm.tab10.colors
    y_positions = {}
    y_pos = 0
    
    for i, (event_type, events) in enumerate(event_types.items()):
        color = colors[i % len(colors)]
        y_positions[event_type] = y_pos
        
        # Plot events as markers
        for event in events:
            ax.plot(event.timestamp, y_pos, 'o', color=color, 
                   markersize=8 * event.intensity + 4, alpha=0.7)
        
        y_pos += 1
    
    # Add event type labels
    for event_type, y_pos in y_positions.items():
        ax.text(-0.1, y_pos, event_type, ha='right', va='center')
    
    # Set axis properties
    ax.set_xlim(-0.2, timestamps[-1] + 0.2)
    ax.set_ylim(-0.5, len(y_positions) - 0.5)
    ax.set_yticks([])
    ax.set_xlabel('Time')
    ax.set_title('Narrative Event Timeline')
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    
    # Save the figure
    output_file = os.path.join("output", "event_timeline.png")
    plt.savefig(output_file)
    plt.close(fig)
    print(f"✓ Saved event timeline to {output_file}")
    
    print("\nSymbolic narrative layer test completed successfully!")
    print("Check the 'output' directory for visualization results and event log.")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    traceback.print_exc()
    print("\nPlease check your implementation and dependencies.")
