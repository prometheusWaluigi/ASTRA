"""
Test script for the ASTRA retrocausal extension (fKPZχ-R).

This script demonstrates the bidirectional time evolution capabilities of ASTRA,
where future states can influence past states through quantum-like retrocausality.
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import traceback
from datetime import datetime

# Create output directory if it doesn't exist
os.makedirs("output", exist_ok=True)

print("Testing ASTRA retrocausal extension (fKPZχ-R)...")

try:
    # Import ASTRA components
    from astra.core.field import QualiaField
    from astra.core.evolution import evolve_chart
    from astra.retrocausal.bidirectional import (
        evolve_bidirectional, 
        compute_temporal_correlation,
        visualize_temporal_correlation
    )
    from astra.retrocausal.boundary import (
        set_future_boundary,
        BoundaryType,
        visualize_boundary_condition
    )
    
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
    
    # First, run standard forward evolution for comparison
    print("\nRunning standard forward evolution for comparison...")
    duration = 1.0  # Simulate 1 time unit
    dt = 0.01        # Time step
    store_frames = 5  # Store 5 frames for analysis
    
    # evolve_chart returns a tuple of (field_history, time_points)
    forward_history, forward_times = evolve_chart(field, duration=duration, dt=dt, store_frames=store_frames)
    
    # Check for NaNs/Infs in forward history
    if np.any(np.isnan(forward_history)) or np.any(np.isinf(forward_history)):
        print("\n❌ Error: NaN or Inf found in standard forward evolution history!")
        # Optional: Exit or raise error if needed
    else:
        print("✓ Forward evolution completed successfully (no NaNs/Infs found)")

    print(f"✓ Forward evolution completed over {len(forward_times)} time steps from t={forward_times[0]} to t={forward_times[-1]}")
    
    # Reset field to initial state
    field.update_state(forward_history[0], 0)
    
    # Create a future boundary condition
    print("\nCreating future boundary condition...")
    boundary = set_future_boundary(
        field_shape=field.get_state().shape,
        boundary_type=BoundaryType.PATTERN,
        pattern='spiral',  # Use a spiral pattern as the future attractor
        time=duration,
        strength=0.7
    )
    
    # Visualize the boundary condition
    fig_boundary, _ = visualize_boundary_condition(boundary, "Spiral Pattern Future Boundary")
    fig_boundary.savefig(os.path.join("output", "future_boundary.png"))
    plt.close(fig_boundary)
    print("✓ Future boundary condition created and visualized")
    
    # Run bidirectional evolution with retrocausal effects
    print("\nRunning bidirectional evolution with retrocausal effects...")
    retro_params = {
        'lambda': 0.1,  # Significantly reduced lambda
        'gamma': 0.05,  # Significantly reduced gamma
        'eta': 0.05,    # Reduced noise level
        'alpha': 1.5    # Standard value for fractional order
    }
    
    retro_results = evolve_bidirectional(
        field=field,
        duration=duration,
        dt=dt,
        retro_strength=0.01,  # Further reduced retro_strength
        boundary_condition=boundary.state,
        n_iterations=2,  # Number of forward-backward iterations
        store_frames=store_frames,
        params=retro_params # Pass the conservative parameters
    )
    retro_history = retro_results['entangled'] # Use 'entangled' key for final history
    retro_times = retro_results['times']
    correlation = retro_results['correlation']
    
    # Check for NaNs/Infs in retro history
    if np.any(np.isnan(retro_history)) or np.any(np.isinf(retro_history)):
        print("\n❌ Error: NaN or Inf found in bidirectional evolution history!")
        # Optional: Exit or raise error if needed
    else:
        print("✓ Bidirectional evolution completed successfully (no NaNs/Infs found)")
    
    print(f"✓ Bidirectional evolution completed over {len(retro_times)} time steps")
    
    # Visualize temporal correlation
    fig_corr, _ = visualize_temporal_correlation(correlation, retro_times, "Temporal Correlation with Retrocausality")
    fig_corr.savefig(os.path.join("output", "temporal_correlation.png"))
    plt.close(fig_corr)
    print("✓ Temporal correlation visualized")
    
    # Compare forward-only and bidirectional evolution
    print("\nComparing forward-only and bidirectional evolution...")
    
    # Create comparison visualization
    fig, axes = plt.subplots(2, len(forward_history), figsize=(15, 8))
    
    # Set global color scale for consistent visualization
    vmin = min(np.min(forward_history), np.min(retro_history))
    vmax = max(np.max(forward_history), np.max(retro_history))
    
    # Plot forward evolution
    for i, (state, time) in enumerate(zip(forward_history, forward_times)):
        ax = axes[0, i]
        im = ax.imshow(state, cmap='viridis', origin='lower', vmin=vmin, vmax=vmax)
        ax.set_title(f"t={time:.2f}")
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Add row label for first column
        if i == 0:
            ax.set_ylabel("Forward Only")
    
    # Plot bidirectional evolution
    for i, (state, time) in enumerate(zip(retro_history, retro_times)):
        ax = axes[1, i]
        im = ax.imshow(state, cmap='viridis', origin='lower', vmin=vmin, vmax=vmax)
        ax.set_title(f"t={time:.2f}")
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Add row label for first column
        if i == 0:
            ax.set_ylabel("Bidirectional")
    
    # Add colorbar
    fig.subplots_adjust(right=0.9)
    cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
    fig.colorbar(im, cax=cbar_ax, label='Field Value')
    
    # Add overall title
    fig.suptitle("Comparison: Forward-Only vs. Bidirectional Evolution", fontsize=16)
    plt.tight_layout(rect=[0, 0, 0.9, 0.95])
    
    # Save the figure
    output_file = os.path.join("output", "evolution_comparison.png")
    plt.savefig(output_file)
    plt.close(fig)
    print(f"✓ Saved comparison visualization to {output_file}")
    
    # Calculate and visualize the difference between forward and bidirectional evolution
    print("\nCalculating retrocausal effects...")
    
    # Create difference visualization
    fig, axes = plt.subplots(1, len(forward_history), figsize=(15, 4))
    
    # Calculate differences
    diff_history = []
    for fwd, retro in zip(forward_history, retro_history):
        diff = retro - fwd
        diff_history.append(diff)
    
    # Set global color scale for differences
    diff_max = max(abs(np.min(diff_history)), abs(np.max(diff_history)))
    vmin_diff = -diff_max
    vmax_diff = diff_max
    
    # Plot differences
    for i, (diff, time) in enumerate(zip(diff_history, forward_times)):
        ax = axes[i]
        im = ax.imshow(diff, cmap='RdBu_r', origin='lower', vmin=vmin_diff, vmax=vmax_diff)
        ax.set_title(f"t={time:.2f}")
        ax.set_xticks([])
        ax.set_yticks([])
    
    # Add colorbar
    fig.subplots_adjust(right=0.9)
    cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
    fig.colorbar(im, cax=cbar_ax, label='Difference (Retrocausal - Forward)')
    
    # Add overall title
    fig.suptitle("Retrocausal Effects: Difference Between Bidirectional and Forward-Only Evolution", fontsize=16)
    plt.tight_layout(rect=[0, 0, 0.9, 0.95])
    
    # Save the figure
    output_file = os.path.join("output", "retrocausal_effects.png")
    plt.savefig(output_file)
    plt.close(fig)
    print(f"✓ Saved retrocausal effects visualization to {output_file}")
    
    # Calculate statistics on retrocausal effects
    mean_diff = [np.mean(np.abs(diff)) for diff in diff_history]
    max_diff = [np.max(np.abs(diff)) for diff in diff_history]
    
    print("\nRetrocausal effect statistics:")
    for i, (time, mean, max_val) in enumerate(zip(forward_times, mean_diff, max_diff)):
        print(f"  Time {time:.2f}: Mean effect = {mean:.4f}, Max effect = {max_val:.4f}")
    
    # Visualize retrocausal effect strength over time
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(forward_times, mean_diff, 'o-', label='Mean Effect')
    ax.plot(forward_times, max_diff, 's-', label='Max Effect')
    ax.set_xlabel('Time')
    ax.set_ylabel('Effect Magnitude')
    ax.set_title('Retrocausal Effect Strength Over Time')
    ax.legend()
    ax.grid(True)
    
    # Save the figure
    output_file = os.path.join("output", "retrocausal_strength.png")
    plt.savefig(output_file)
    plt.close(fig)
    print(f"✓ Saved retrocausal strength plot to {output_file}")
    
    print("\nRetrocausal extension test completed successfully!")
    print("Check the 'output' directory for visualization results.")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    traceback.print_exc()
    print("\nPlease check your implementation and dependencies.")
