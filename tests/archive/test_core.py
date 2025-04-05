"""
Simple test script for the ASTRA core functionality.
This script creates a mock natal chart and tests the QualiaField and evolution.
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import traceback

# Add detailed error reporting
def exception_handler(exc_type, exc_value, exc_traceback):
    print("\n*** Uncaught Exception ***")
    traceback.print_exception(exc_type, exc_value, exc_traceback)
    print("\n")
sys.excepthook = exception_handler

# Create output directory if it doesn't exist
os.makedirs("output", exist_ok=True)

print("Testing ASTRA core functionality...")

try:
    # Import ASTRA core components
    from astra.core import QualiaField, evolve_chart
    print("✓ Successfully imported ASTRA core modules")
    
    # Create a mock natal data object (similar structure to Kerykeion's AstrologicalSubject)
    class MockNatalData:
        def __init__(self):
            self.name = "Test Subject"
            
            # Mock planets with positions
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
    
    # Create mock natal data (based on Jan 4, 1985, 5am, Minneapolis)
    mock_natal = MockNatalData()
    print("✓ Created mock natal data")
    
    # Initialize QualiaField with smaller grid for faster testing
    print("\nInitializing QualiaField...")
    field = QualiaField(mock_natal, grid_size=(64, 64))
    print("✓ QualiaField initialized")
    
    # Save initial field visualization
    print("\nSaving initial field visualization...")
    fig, ax = plt.subplots(figsize=(8, 6))
    field.visualize(ax=ax, show=False)
    output_file = os.path.join("output", "initial_field.png")
    plt.savefig(output_file)
    plt.close(fig)
    print(f"✓ Saved to {output_file}")
    
    # Evolve the field for a short duration
    print("\nEvolving field...")
    field_history, time_points = evolve_chart(field, duration=0.5, dt=0.01, store_frames=3)
    print(f"✓ Field evolved to t={field.time:.3f}")
    print(f"✓ Stored {len(field_history)} frames at times: {time_points}")
    
    # Save evolution visualization
    print("\nSaving evolution visualization...")
    n_frames = len(field_history)
    cols = min(3, n_frames)
    rows = (n_frames + cols - 1) // cols
    
    fig, axes = plt.subplots(rows, cols, figsize=(12, 8))
    if rows == 1 and cols == 1:
        axes = np.array([axes])
    axes = axes.flatten()
    
    vmin = min(np.min(f) for f in field_history)
    vmax = max(np.max(f) for f in field_history)
    
    for i, (field_state, t) in enumerate(zip(field_history, time_points)):
        if i < len(axes):
            im = axes[i].imshow(field_state, origin='lower', cmap='viridis', 
                              interpolation='nearest', vmin=vmin, vmax=vmax)
            axes[i].set_title(f"t = {t:.2f}")
            axes[i].set_xticks([])
            axes[i].set_yticks([])
    
    for i in range(n_frames, len(axes)):
        axes[i].axis('off')
    
    fig.subplots_adjust(right=0.9)
    cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
    fig.colorbar(im, cax=cbar_ax, label='χ(x,t) magnitude')
    
    fig.suptitle("QualiaField Evolution", fontsize=16)
    plt.tight_layout(rect=[0, 0, 0.9, 0.95])
    
    output_file = os.path.join("output", "field_evolution.png")
    plt.savefig(output_file)
    plt.close(fig)
    print(f"✓ Saved to {output_file}")
    
    print("\nTest completed successfully!")
    print("Check the 'output' directory for visualization results.")

except Exception as e:
    print(f"\n❌ Error: {e}")
    traceback.print_exc()
    print("\nPlease check your implementation and dependencies.")
