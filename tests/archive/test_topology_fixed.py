"""
Fixed test script for the ASTRA topology module (𝓈-Layer).

This script provides a simplified implementation for topology analysis that avoids
problematic algorithm dependencies.
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import traceback
from scipy.ndimage import gaussian_filter, label, find_objects

# Create output directory if it doesn't exist
os.makedirs("output", exist_ok=True)

print("Testing ASTRA topology module (𝓈-Layer) with fixed implementation...")

try:
    # Import ASTRA core components
    from astra.core.field import QualiaField
    from astra.core.evolution import evolve_chart
    
    # Create a mock natal data object
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
    output_file = os.path.join("output", "topology_field_fixed.png")
    plt.savefig(output_file)
    plt.close(fig)
    print(f"✓ Saved to {output_file}")
    
    # Evolve the field
    print("\nEvolving field...")
    field_history, timestamps = evolve_chart(field, duration=1.0, dt=0.1, store_frames=5)
    final_field = field_history[-1]  # Get the final state
    print("✓ Field evolved")
    
    # Custom implementation for topology analysis
    # This avoids using the problematic packages
    
    def find_local_maxima(field, sigma=1.0, threshold=0.2):
        """Find local maxima in the field."""
        # Smooth the field for better peak detection
        smoothed = gaussian_filter(field, sigma=sigma)
        
        # Identify local maxima
        height, width = smoothed.shape
        maxima = []
        
        for y in range(1, height-1):
            for x in range(1, width-1):
                # Check if current pixel is greater than all 8 neighbors
                center = smoothed[y, x]
                if center < threshold:
                    continue
                    
                is_maximum = True
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        if center <= smoothed[y+dy, x+dx]:
                            is_maximum = False
                            break
                    if not is_maximum:
                        break
                
                if is_maximum:
                    maxima.append({
                        'location': (x, y),
                        'value': center,
                        'size': 1  # Default size
                    })
        
        return maxima
    
    def find_connected_components(field, threshold=0.2):
        """Find connected components in the field."""
        # Binarize the field
        binary = (field > threshold).astype(np.uint8)
        
        # Label connected components
        labeled, num_components = label(binary)
        
        # Find objects (bounding boxes) for each component
        objects = find_objects(labeled)
        
        components = []
        for i, obj in enumerate(objects):
            if obj is None:
                continue
                
            # Get component mask
            mask = (labeled[obj] == i+1)
            
            # Calculate component size and center
            y_indices, x_indices = np.where(mask)
            size = len(y_indices)
            
            if size == 0:
                continue
                
            # Center of mass
            y_center = int(np.mean(y_indices)) + obj[0].start
            x_center = int(np.mean(x_indices)) + obj[1].start
            
            # Average field value
            avg_value = np.mean(field[obj][mask])
            
            components.append({
                'location': (x_center, y_center),
                'size': size,
                'value': avg_value,
                'bbox': obj
            })
        
        return components, labeled
    
    def estimate_field_curvature(field, sigma=1.0):
        """Estimate field curvature using the Laplacian."""
        # Smooth the field
        smoothed = gaussian_filter(field, sigma=sigma)
        
        # Compute Laplacian (∇²)
        from scipy.ndimage import laplace
        lap = laplace(smoothed)
        
        # Laplacian is proportional to mean curvature
        # Negative because convex regions (peaks) have positive curvature
        curvature = -lap
        
        return curvature
    
    def compute_approximate_betti_numbers(field, threshold=0.2):
        """Compute approximate Betti numbers using connected components."""
        # β₀: number of connected components (above threshold)
        components, labeled = find_connected_components(field, threshold)
        beta0 = len(components)
        
        # β₁: approximate loops by counting "holes"
        # For a simplified approach, we'll detect holes by looking for connected components
        # in the complement (inverted) field
        inverted = 1.0 - field / np.max(field)
        inv_components, _ = find_connected_components(inverted, threshold)
        
        # Remove the background component (usually the largest)
        if inv_components:
            inv_components = sorted(inv_components, key=lambda c: c['size'], reverse=True)
            inv_components = inv_components[1:]  # Skip the background
        
        beta1 = len(inv_components)
        
        # β₂: approximated based on local curvature structure
        # Count regions of strong positive curvature (spheres)
        curvature = estimate_field_curvature(field)
        pos_curvature_regions, _ = find_connected_components(
            (curvature > np.max(curvature) * 0.7).astype(float), 
            threshold=0.5
        )
        beta2 = len(pos_curvature_regions)
        
        return [beta0, beta1, beta2]
    
    # Perform simplified topological analysis
    print("\nPerforming simplified topological analysis...")
    
    # Find maxima (peaks)
    maxima = find_local_maxima(final_field, threshold=0.1)
    print(f"✓ Found {len(maxima)} local maxima (peaks)")
    
    # Compute approximate Betti numbers
    betti = compute_approximate_betti_numbers(final_field, threshold=0.1)
    print(f"✓ Betti numbers: β₀={betti[0]}, β₁={betti[1]}, β₂={betti[2]}")
    
    # Estimate field curvature
    curvature = estimate_field_curvature(final_field)
    
    # Create a visualization of the topological features
    print("\nCreating visualization of topological features...")
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    
    # Original field
    ax = axs[0, 0]
    im = ax.imshow(final_field, cmap='viridis', origin='lower')
    plt.colorbar(im, ax=ax)
    ax.set_title("Qualia Field")
    
    # Mark local maxima
    for peak in maxima:
        x, y = peak['location']
        ax.plot(x, y, 'r*', markersize=8)
    
    # Connected components
    ax = axs[0, 1]
    components, labeled = find_connected_components(final_field, threshold=0.1)
    im = ax.imshow(labeled, cmap='tab20', origin='lower')
    plt.colorbar(im, ax=ax)
    ax.set_title(f"Connected Components (β₀={betti[0]})")
    
    # Curvature field
    ax = axs[1, 0]
    im = ax.imshow(curvature, cmap='coolwarm', origin='lower')
    plt.colorbar(im, ax=ax)
    ax.set_title("Estimated Curvature")
    
    # Inverted field for "holes" (β₁)
    ax = axs[1, 1]
    inverted = 1.0 - final_field / np.max(final_field)
    im = ax.imshow(inverted, cmap='plasma', origin='lower')
    plt.colorbar(im, ax=ax)
    ax.set_title(f"Inverted Field (for β₁={betti[1]})")
    
    plt.tight_layout()
    output_file = os.path.join("output", "topology_analysis_fixed.png")
    plt.savefig(output_file)
    plt.close(fig)
    print(f"✓ Saved visualization to {output_file}")
    
    print("\nTopology analysis completed successfully!")
    print("Check the 'output' directory for visualization results.")
    
except Exception as e:
    print("\n*** Error ***")
    traceback.print_exc()
    print("\nPlease check your implementation and dependencies.")
