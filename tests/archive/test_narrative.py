"""
Test script for the ASTRA symbolic narrative layer (𝓂-Layer).

This script demonstrates the narrative generation capabilities of ASTRA,
generating symbolic interpretations of the qualia field's topological patterns.
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import traceback
from datetime import datetime

# Create output directory if it doesn't exist
os.makedirs("output", exist_ok=True)

print("Testing ASTRA symbolic narrative layer (𝓂-Layer)...")

try:
    # Import ASTRA components
    from astra.core.field import QualiaField
    from astra.core.evolution import evolve_chart
    from astra.symbols.narrative import generate_narrative, create_event_log, NarrativeEvent, EventType
    from astra.symbols.threshold import detect_threshold_crossings, detect_phase_transitions
    
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
    
    # Generate narratives for each time step
    print("\nGenerating symbolic narratives...")
    all_events = []
    
    for i in range(1, len(field_history)):
        current_field = field_history[i]
        prev_field = field_history[i-1]
        timestamp = timestamps[i]
        
        # Generate narrative events using simplified path
        narrative_events = generate_narrative(
            field=current_field, 
            prev_field=prev_field,
            timestamp=timestamp,
            detect_motifs=False  # Use simplified path without topology
        )
        
        # Detect threshold crossings
        threshold_events = detect_threshold_crossings(
            current_field,
            previous_field=prev_field,
            timestamp=timestamp
        )
        
        # Convert threshold events to narrative events
        for event in threshold_events:
            narrative_events.append(event.to_narrative_event())
        
        all_events.extend(narrative_events)
        
        print(f"  Time {timestamp:.2f}: Generated {len(narrative_events)} events")
    
    # Detect phase transitions across the entire history
    print("\nDetecting phase transitions...")
    phase_transitions = detect_phase_transitions(field_history, timestamps)
    
    # Convert phase transitions to narrative events
    for event in phase_transitions:
        all_events.append(event.to_narrative_event())
    
    print(f"✓ Detected {len(phase_transitions)} phase transitions")
    
    # Create event log
    print("\nCreating event log...")
    event_log = create_event_log(all_events, output_file="output/narrative_events.json")
    print(f"✓ Created event log with {len(all_events)} events")
    
    # Display some sample events
    print("\nSample narrative events:")
    for i, event in enumerate(sorted(all_events, key=lambda e: e.timestamp)[:5]):
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
            if event.location:
                y, x = event.location
                ax.plot(x, y, 'ro', markersize=10, alpha=0.7)
                
                # Add event type as text
                ax.text(x+2, y+2, event.event_type.name[:4], color='white', 
                       fontsize=8, bbox=dict(facecolor='red', alpha=0.5))
    
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
