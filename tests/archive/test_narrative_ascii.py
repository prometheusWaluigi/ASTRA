"""
ASCII-safe version of narrative test for ASTRA

Tests the simplified narrative generation without Unicode characters
"""

import os
import sys
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple

# Make sure we can import from the astra package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import ASTRA modules
try:
    from astra.core import QualiaField, evolve
    print("[PASS] Successfully imported ASTRA core modules")
except ImportError as e:
    print(f"[ERROR] Failed to import ASTRA core modules: {e}")
    sys.exit(1)

# Create output directory if it doesn't exist
os.makedirs("output", exist_ok=True)
os.makedirs("output/narrative", exist_ok=True)

print("Testing ASTRA symbolic narrative layer with simple implementation...")

# Define custom JSON encoder to handle NumPy and complex types
class ASTRAJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, complex):
            return {"real": obj.real, "imag": obj.imag}
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

# Simple event detector function
def detect_events(field: np.ndarray, threshold: float = 0.75) -> List[Dict[str, Any]]:
    """
    Detect narrative events in a field based on simple thresholding.
    
    Args:
        field: 2D numpy array representing the qualia field
        threshold: Percentile threshold for determining significant features
        
    Returns:
        List of detected events
    """
    events = []
    
    # Find peaks (areas above threshold)
    high_threshold = np.percentile(field, threshold * 100)
    peak_regions = (field > high_threshold)
    
    # Find valleys (areas below negative threshold)
    low_threshold = np.percentile(field, (1 - threshold) * 100)
    valley_regions = (field < low_threshold)
    
    # Count connected regions (simplified)
    peak_count = np.sum(peak_regions)
    valley_count = np.sum(valley_regions)
    
    # Create emergence events for peaks
    if peak_count > 0:
        # Find center of mass for the largest peak
        weighted_coords = np.where(peak_regions)
        if len(weighted_coords[0]) > 0:
            y_center = int(np.mean(weighted_coords[0]))
            x_center = int(np.mean(weighted_coords[1]))
            
            # Calculate intensity
            intensity = np.mean(field[peak_regions])
            
            events.append({
                "type": "EMERGENCE",
                "location": (y_center, x_center),
                "intensity": float(intensity),
                "size": int(peak_count)
            })
    
    # Create dissolution events for valleys
    if valley_count > 0:
        # Find center of mass for the largest valley
        weighted_coords = np.where(valley_regions)
        if len(weighted_coords[0]) > 0:
            y_center = int(np.mean(weighted_coords[0]))
            x_center = int(np.mean(weighted_coords[1]))
            
            # Calculate intensity (absolute value)
            intensity = abs(np.mean(field[valley_regions]))
            
            events.append({
                "type": "DISSOLUTION",
                "location": (y_center, x_center),
                "intensity": float(intensity),
                "size": int(valley_count)
            })
    
    # Add archetype events based on field patterns
    field_mean = np.mean(field)
    field_std = np.std(field)
    
    # Hero archetype - strong positive deviation
    if field_mean > 0 and field_std > 0.5:
        events.append({
            "type": "THE_HERO",
            "intensity": float(field_mean + field_std),
            "confidence": min(1.0, float(field_std))
        })
    
    # Mentor archetype - moderate positive values with low variance
    if field_mean > 0 and field_std < 0.3:
        events.append({
            "type": "THE_MENTOR",
            "intensity": float(field_mean),
            "confidence": min(1.0, float(1.0 - field_std))
        })
    
    return events

# Generate and interpret a narrative sequence
def generate_narrative(duration: float = 1.0, steps: int = 5) -> Dict[str, Any]:
    """
    Generate a narrative sequence from an evolving field.
    
    Args:
        duration: Total evolution time
        steps: Number of narrative time steps
        
    Returns:
        Dictionary with narrative sequence information
    """
    # Create initial field
    field = QualiaField(grid_size=64)
    initial_field = field.grid.copy()
    
    # Calculate time step
    dt = duration / steps
    
    # Prepare to store frames and events
    frames = []
    all_events = []
    
    # Store initial state
    frames.append(initial_field.copy())
    initial_events = detect_events(initial_field)
    all_events.append(initial_events)
    
    # Evolve field and detect events at each step
    current_field = initial_field.copy()
    
    for step in range(steps):
        # Evolve the field
        evolution_result = evolve(
            current_field,
            duration=dt,
            dt=0.01,
            alpha=0.5,
            beta=0.9,
            gamma=0.3,
            store_frames=2  # Only store start and end
        )
        
        # Get the evolved field
        current_field = evolution_result["final_state"]
        
        # Store the frame
        frames.append(current_field.copy())
        
        # Detect events
        events = detect_events(current_field)
        all_events.append(events)
        
        print(f"[STEP {step+1}] Detected {len(events)} events")
    
    # Create the narrative sequence
    narrative = {
        "frames": frames,
        "events": all_events,
        "duration": duration,
        "steps": steps,
        "timestamp": datetime.now().isoformat()
    }
    
    return narrative

# Generate a narrative
print("Generating narrative sequence...")
narrative = generate_narrative(duration=1.0, steps=5)
print(f"[PASS] Generated narrative with {len(narrative['frames'])} frames")

# Save narrative to JSON
try:
    narrative_path = "output/narrative/narrative_sequence.json"
    with open(narrative_path, "w") as f:
        json.dump(narrative, f, cls=ASTRAJSONEncoder, indent=2)
    print(f"[PASS] Saved narrative to {narrative_path}")
except Exception as e:
    print(f"[ERROR] Failed to save narrative to JSON: {str(e)}")

# Visualize the narrative sequence
print("Creating narrative visualization...")
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
axes = axes.flatten()

# Show a sample of frames
for i in range(min(6, len(narrative["frames"]))):
    ax = axes[i]
    ax.imshow(narrative["frames"][i], cmap='viridis')
    
    # Add event markers
    events = narrative["events"][i]
    for event in events:
        if "location" in event:
            y, x = event["location"]
            ax.plot(x, y, 'ro', markersize=10)
            ax.text(x + 5, y, event["type"], color='white', fontsize=8, 
                    bbox=dict(facecolor='black', alpha=0.5))
    
    # Add title with event count
    ax.set_title(f"Frame {i}: {len(events)} events")
    ax.set_xticks([])
    ax.set_yticks([])

plt.tight_layout()
plt.savefig("output/narrative/narrative_sequence.png")
plt.close()
print("[PASS] Narrative visualization saved to output/narrative/narrative_sequence.png")

# Create a summary of detected events
event_counts = [len(events) for events in narrative["events"]]
print("Event summary:")
for i, count in enumerate(event_counts):
    print(f"  Frame {i}: {count} events")

total_events = sum(event_counts)
print(f"Total events detected: {total_events}")

# Plot event counts
plt.figure(figsize=(10, 6))
plt.bar(range(len(event_counts)), event_counts)
plt.xlabel('Frame')
plt.ylabel('Number of Events')
plt.title('Event Count per Frame')
plt.savefig("output/narrative/event_counts.png")
plt.close()
print("[PASS] Event count visualization saved to output/narrative/event_counts.png")

print("Narrative tests completed successfully!")
