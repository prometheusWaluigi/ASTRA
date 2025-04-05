"""
Simplified test script for the ASTRA topology module (𝓈-Layer).

This script demonstrates the basic topological analysis capabilities of ASTRA,
using a simplified approach that doesn't rely on optional dependencies.
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import traceback
from scipy.ndimage import gaussian_filter

# Create output directory if it doesn't exist
os.makedirs("output", exist_ok=True)

print("Testing ASTRA topology module (𝓈-Layer) with simplified approach...")

try:
    # Import ASTRA core components
    from astra.core.field import QualiaField
    
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
    
    # Get the field state
    field_state = field.get_state()
    
    # Save field visualization
    print("\nSaving field visualization...")
    fig, ax = plt.subplots(figsize=(8, 6))
    field.visualize(ax=ax, show=False)
    output_file = os.path.join("output", "topology_field.png")
    plt.savefig(output_file)
    plt.close(fig)
    print(f"✓ Saved to {output_file}")
    
    # Simplified topological analysis
    print("\nPerforming simplified topological analysis...")
    
    # 1. Find local maxima (peaks)
    from scipy.ndimage import maximum_filter, label
    
    # Smooth the field to reduce noise
    smoothed = gaussian_filter(field_state, sigma=1.0)
    
    # Find local maxima
    max_filtered = maximum_filter(smoothed, size=3)
    maxima = (smoothed == max_filtered) & (smoothed != smoothed.min())
    maxima_coords = np.argwhere(maxima)
    
    print(f"✓ Found {len(maxima_coords)} local maxima (peaks)")
    
    # 2. Identify connected components (simplified β₀)
    # Threshold the field to focus on significant values
    threshold = np.mean(smoothed)
    binary = smoothed > threshold
    
    # Label connected components
    labeled, num_components = label(binary)
    
    print(f"✓ Found {num_components} connected components (β₀)")
    
    # 3. Detect "loops" (simplified β₁) by looking for holes in the binary image
    # Invert the binary image to look for holes
    inverted = ~binary
    labeled_holes, num_holes = label(inverted)
    
    # Exclude the background (largest component)
    sizes = np.bincount(labeled_holes.ravel())
    largest_hole = np.argmax(sizes[1:]) + 1 if len(sizes) > 1 else 0
    
    # Count non-background holes
    true_holes = max(0, num_holes - (1 if largest_hole > 0 else 0))
    
    print(f"✓ Found approximately {true_holes} loops/cycles (β₁)")
    
    # 4. Compute "joy" as areas of high curvature (simplified)
    from scipy.ndimage import laplace
    
    # Compute Laplacian as a simple curvature measure
    lap = laplace(smoothed)
    
    # Negative Laplacian approximates negative curvature (joy)
    joy = -lap
    
    # Visualize the results
    print("\nCreating visualization of topological features...")
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Original field
    im1 = axes[0, 0].imshow(field_state, cmap='viridis', origin='lower')
    axes[0, 0].set_title("Qualia Field χ(x,t)")
    plt.colorbar(im1, ax=axes[0, 0])
    
    # Connected components
    im2 = axes[0, 1].imshow(labeled, cmap='tab20', origin='lower')
    axes[0, 1].set_title(f"Connected Components (β₀={num_components})")
    plt.colorbar(im2, ax=axes[0, 1])
    
    # Maxima (peaks)
    axes[1, 0].imshow(smoothed, cmap='viridis', origin='lower')
    axes[1, 0].scatter(maxima_coords[:, 1], maxima_coords[:, 0], 
                     color='red', marker='o', s=50)
    axes[1, 0].set_title(f"Local Maxima ({len(maxima_coords)} peaks)")
    
    # Joy field (negative curvature)
    im4 = axes[1, 1].imshow(joy, cmap='RdBu_r', origin='lower')
    axes[1, 1].set_title("Joy Field (Negative Curvature)")
    plt.colorbar(im4, ax=axes[1, 1])
    
    # Add overall title
    plt.suptitle(f"Topological Analysis of Qualia Field\nJan 4, 1985 - Minneapolis", fontsize=16)
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    output_file = os.path.join("output", "topology_analysis.png")
    plt.savefig(output_file)
    plt.close(fig)
    print(f"✓ Saved visualization to {output_file}")
    
    print("\nSimplified topology analysis completed successfully!")
    print("Check the 'output' directory for visualization results.")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    traceback.print_exc()
    print("\nPlease check your implementation and dependencies.")
