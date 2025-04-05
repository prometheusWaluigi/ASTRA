"""
ASCII-safe version of test_enhanced.py for ASTRA

Tests the enhanced fKPZ implementation without Unicode characters
"""

import os
import sys
import time
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Make sure we can import from the astra package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import ASTRA modules
try:
    from astra.core import QualiaField, evolve_step, evolve
    print("[PASS] Successfully imported ASTRA core modules")
except ImportError as e:
    print(f"[ERROR] Failed to import ASTRA core modules: {e}")
    sys.exit(1)

print("Testing ASTRA enhanced fKPZ implementation...")

# Create output directory if it doesn't exist
os.makedirs("output", exist_ok=True)
os.makedirs("output/enhanced", exist_ok=True)

# Create a larger QualiaField for more detailed simulations
print("Creating enhanced QualiaField...")
field = QualiaField(grid_size=128)
print(f"[PASS] Created QualiaField with shape {field.grid.shape}")

# Save initial state
plt.figure(figsize=(10, 8))
plt.imshow(field.grid, cmap='viridis')
plt.colorbar(label='Field Value')
plt.title('Initial Qualia Field')
plt.savefig("output/enhanced/initial_state.png")
plt.close()
print("[PASS] Initial state saved to output/enhanced/initial_state.png")

# Parameters for different field evolutions
evolution_params = {
    "meditation": {
        "alpha": 0.3,  # Reduced non-linearity for smoother patterns
        "beta": 0.8,   # Medium noise level
        "gamma": 0.2,  # Low symmetry breaking
        "duration": 1.0,
        "dt": 0.01
    },
    "joy": {
        "alpha": 0.7,  # Higher non-linearity for more complex patterns
        "beta": 1.2,   # Higher noise level for more activity
        "gamma": 0.4,  # Medium symmetry breaking
        "duration": 1.0,
        "dt": 0.01
    },
    "coherence": {
        "alpha": 0.5,  # Balanced non-linearity
        "beta": 0.5,   # Lower noise for clearer patterns
        "gamma": 0.1,  # Minimal symmetry breaking for stable structures
        "duration": 1.0,
        "dt": 0.01
    }
}

# Evolve the field with different parameter sets
results = {}
for state_name, params in evolution_params.items():
    print(f"Evolving field for state: {state_name}...")
    start_time = time.time()
    
    # Use the full evolve function
    evolution_result = evolve(
        field.grid.copy(),
        duration=params["duration"],
        dt=params["dt"],
        alpha=params["alpha"],
        beta=params["beta"],
        gamma=params["gamma"],
        store_frames=10
    )
    
    evolved_field = evolution_result["final_state"]
    frames = evolution_result["frames"]
    
    duration = time.time() - start_time
    print(f"[PASS] Evolution completed in {duration:.2f} seconds")
    
    # Save the result
    plt.figure(figsize=(10, 8))
    plt.imshow(evolved_field, cmap='viridis')
    plt.colorbar(label='Field Value')
    plt.title(f'Evolved Field - {state_name.capitalize()}')
    plt.savefig(f"output/enhanced/{state_name}_final.png")
    plt.close()
    
    # Store the result
    results[state_name] = {
        "field": evolved_field,
        "frames": frames,
        "params": params
    }
    
    print(f"[PASS] {state_name.capitalize()} state saved to output/enhanced/{state_name}_final.png")

# Compare the fields
print("Creating comparison visualization...")
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

for i, (state_name, result) in enumerate(results.items()):
    axes[i].imshow(result["field"], cmap='viridis')
    axes[i].set_title(f'{state_name.capitalize()}')
    axes[i].set_xticks([])
    axes[i].set_yticks([])

plt.savefig("output/enhanced/state_comparison.png")
plt.close()
print("[PASS] Comparison visualization saved to output/enhanced/state_comparison.png")

print("All enhanced tests passed!")
