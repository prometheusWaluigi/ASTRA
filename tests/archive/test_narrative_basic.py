"""
Basic test script for the ASTRA symbolic narrative layer (𝓂-Layer).

This script demonstrates the narrative generation capabilities of ASTRA
without relying on complex JSON serialization or the full topology module.
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import traceback
from datetime import datetime
from enum import Enum, auto

# Create output directory if it doesn't exist
os.makedirs("output", exist_ok=True)

print("Testing ASTRA symbolic narrative layer (𝓂-Layer) with basic approach...")

# Define a simple NarrativeEvent class for testing if not imported
# NarrativeEvent class now imported from astra.symbols.narrative

try:
    # Import ASTRA components
    from astra.core.field import QualiaField
    from astra.core.evolution import evolve_chart
    from astra.symbols.narrative import NarrativeEvent, EventType, interpret_motifs, generate_narrative

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
    
    # Define archetypal patterns
    ARCHETYPAL_PATTERNS = {
        'RECURSIVE_LOOP': {
            'name': 'Recursive Loop',
            'description': 'A self-referential thought pattern creating a feedback loop',
            'narrative_templates': [
                "A recursive pattern emerges, creating a self-referential loop in consciousness",
                "Thoughts begin to circle back on themselves, creating a recursive structure",
                "A self-reflective loop forms, allowing consciousness to observe itself"
            ]
        },
        'EGO_CONDENSATION': {
            'name': 'Ego Condensation',
            'description': 'Crystallization of identity structures',
            'narrative_templates': [
                "The ego structure crystallizes, creating a stronger sense of self",
                "Identity boundaries form and solidify, creating a distinct sense of 'I'",
                "A condensation of self-concept occurs, strengthening ego structures"
            ]
        },
        'DISSOLUTION': {
            'name': 'Dissolution',
            'description': 'Boundary dissolution, ego death',
            'narrative_templates': [
                "Boundaries begin to dissolve, creating a sense of unity with the field",
                "Ego structures temporarily dissolve, allowing for transcendent experience",
                "A dissolution of identity boundaries occurs, opening to larger consciousness"
            ]
        },
        'INTEGRATION': {
            'name': 'Integration',
            'description': 'Integration of disparate elements',
            'narrative_templates': [
                "Previously separate elements integrate into a coherent whole",
                "A synthesis occurs, bringing together disparate aspects of consciousness",
                "An integration process begins, harmonizing conflicting elements"
            ]
        }
    }
    
    # Generate simplified narratives
    print("\nGenerating symbolic narratives...")
    all_events = []
    
    # Generate narratives for each time step using simplified approach
    for i in range(1, len(field_history)):
        current_field = field_history[i]
        prev_field = field_history[i-1]
        timestamp = timestamps[i]
        
        # Generate narrative events using the simplified path
        events_for_timestep = generate_narrative(
            field=current_field,
            prev_field=prev_field,
            timestamp=timestamp,
            detect_motifs=False  # Use simplified path without topology
        )
        
        # Add events for this timestep to overall list
        all_events.extend(events_for_timestep)
        print(f"  Time {timestamp:.2f}: Generated {len(events_for_timestep)} events")
    
    # Display some sample events
    print("\nSample narrative events:")
    for i, event in enumerate(sorted(all_events, key=lambda e: e.timestamp)[:5]):
        print(f"  {i+1}. {event}")
    
    # Create visualization of field evolution
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
    
    def create_test_qualia_field():
        # Create a simple qualia field with an attractor (potential Mentor)
        # and a high persistence value at a certain location (potential Hero)
        size = 20
        field = np.zeros((size, size))
        # Attractor (Mentor)
        field[5:8, 5:8] = 0.7
        # Hero (high persistence)
        field[10:12, 10:12] = 0.9
        return field
    
    def test_narrative_generation():
        field = create_test_qualia_field()
        timestamp = 0.0
        
        # Generate narrative events (using field only)
        events = generate_narrative(
            field=field,
            timestamp=timestamp,
            detect_motifs=False  # Use simplified path without topology
        )
        
        # Print the generated events
        print("Generated Narrative Events:")
        for event in events:
            print(f"  Timestamp: {event.timestamp}")
            print(f"  Event Type: {event.event_type}")
            print(f"  Description: {event.description}")
            print(f"  Intensity: {event.intensity}")
    
    # Run the test
    test_narrative_generation()
    
    print("\nSymbolic narrative layer test completed successfully!")
    print("Check the 'output' directory for visualization results.")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    traceback.print_exc()
    print("\nPlease check your implementation and dependencies.")
