"""
Test script for the ASTRA topology module (𝓈-Layer).

This script demonstrates the topological analysis capabilities of ASTRA,
analyzing the qualia field generated from a birth chart to detect:
- Persistent homology features (connected components, loops, voids)
- Ricci curvature and joy fields
- Topological motifs and attractor types

These analyses reveal the deeper structure of consciousness as modeled by the fKPZχ equation.
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

print("Testing ASTRA topology module (𝓈-Layer)...")

try:
    # Import ASTRA components
    from astra.core.field import QualiaField
    from astra.core.evolution_enhanced import evolve_chart_enhanced
    
    # Import topology components
    from astra.topology.persistence import (
        compute_persistence_diagram,
        compute_betti_numbers,
        plot_persistence_diagram
    )
    
    # Use the safer implementation for Ricci curvature
    from astra.topology.ricci_safe import (
        compute_ollivier_ricci_curvature,
        compute_joy_field,
        plot_ricci_curvature
    )
    from astra.topology.motifs import (
        detect_topological_motifs,
        classify_attractor_type,
        plot_attractor_landscape
    )
    
    print("✓ Successfully imported ASTRA modules")
    
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
    
    # Define enhanced parameters based on the mathematical formulation
    enhanced_params = {
        'nu': 1.0,                # Diffusion coefficient
        'lambda': 0.5,            # Base nonlinearity parameter (Sun)
        'alpha': 0.5,             # Fractional Laplacian order (d_q - 1, where d_q = 1.5)
        'beta': 1.1,              # Fractional gradient order (1 + δ)
        'gamma': 0.2,             # Symmetry breaking strength (Ascendant)
        'kappa': 2.0,             # Identity structure sharpness
        'eta': 0.1,               # Noise amplitude (Moon)
        'noise_type': 'fractal',  # Type of noise
        'hurst': 0.7,             # Hurst exponent for fractal noise
        'theta': 0.0,             # Initial meditation modulation
        'dt': 0.01                # Time step
    }
    
    # Initialize QualiaField
    print("\nInitializing QualiaField...")
    field = QualiaField(mock_natal, grid_size=(128, 128))
    print("✓ QualiaField initialized")
    
    # Save initial field visualization
    print("\nSaving initial field visualization...")
    fig, ax = plt.subplots(figsize=(8, 6))
    field.visualize(ax=ax, show=False)
    output_file = os.path.join("output", "topology_initial_field.png")
    plt.savefig(output_file)
    plt.close(fig)
    print(f"✓ Saved to {output_file}")
    
    # Evolve the field
    print("\nEvolving field...")
    result = evolve_chart_enhanced(
        field, 
        duration=0.5, 
        params=enhanced_params, 
        store_frames=3,
        compute_metrics=True
    )
    print(f"✓ Field evolved")
    
    # Get the final field state
    final_field = result['field_history'][-1]
    
    # 1. Persistent Homology Analysis
    print("\nComputing persistent homology...")
    persistence_result = compute_persistence_diagram(final_field, max_dim=2)
    betti_numbers = compute_betti_numbers(persistence_result['diagrams'])
    
    print(f"✓ Betti numbers: β₀={betti_numbers[0]}, β₁={betti_numbers[1]}, β₂={betti_numbers[2]}")
    
    # Plot persistence diagram
    fig, ax = plt.subplots(figsize=(8, 8))
    plot_persistence_diagram(persistence_result['diagrams'], 
                           title="Persistence Diagram for Qualia Field", 
                           ax=ax)
    output_file = os.path.join("output", "persistence_diagram.png")
    plt.savefig(output_file)
    plt.close(fig)
    print(f"✓ Saved persistence diagram to {output_file}")
    
    # 2. Ricci Curvature Analysis
    print("\nComputing Ricci curvature...")
    G, curvature_field = compute_ollivier_ricci_curvature(final_field, threshold=0.0)
    
    # Compute joy field
    joy_field = compute_joy_field(final_field)
    
    # Plot Ricci curvature
    fig, ax = plt.subplots(figsize=(10, 8))
    plot_ricci_curvature(G, final_field, curvature_field, 
                        title="Ricci Curvature of Qualia Field", 
                        ax=ax)
    output_file = os.path.join("output", "ricci_curvature.png")
    plt.savefig(output_file)
    plt.close(fig)
    print(f"✓ Saved Ricci curvature to {output_file}")
    
    # Plot joy field
    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(joy_field, cmap='RdBu_r', origin='lower')
    plt.colorbar(im, ax=ax, label='Joy (-Ric)')
    ax.set_title("Joy Field (Negative Ricci Curvature)")
    output_file = os.path.join("output", "joy_field.png")
    plt.savefig(output_file)
    plt.close(fig)
    print(f"✓ Saved joy field to {output_file}")
    
    # 3. Topological Motifs Analysis
    print("\nDetecting topological motifs...")
    motifs_result = detect_topological_motifs(final_field)
    
    # Print detected motifs
    print("Detected motifs:")
    for motif in motifs_result['motifs']:
        print(f"  - {motif['name']}: {motif['description']} (confidence: {motif['confidence']:.2f})")
    
    # 4. Attractor Classification
    print("\nClassifying attractor type...")
    attractor_result = classify_attractor_type(final_field)
    
    print(f"✓ Attractor type: {attractor_result['attractor_type']} ({attractor_result['confidence']:.2f} confidence)")
    print(f"  {attractor_result['description']}")
    
    # Plot attractor landscape
    fig, ax = plt.subplots(figsize=(10, 8))
    plot_attractor_landscape(final_field, attractor_result, ax=ax)
    output_file = os.path.join("output", "attractor_landscape.png")
    plt.savefig(output_file)
    plt.close(fig)
    print(f"✓ Saved attractor landscape to {output_file}")
    
    # 5. Combined Analysis Report
    print("\nGenerating combined topological analysis report...")
    
    # Create a multi-panel figure
    fig = plt.figure(figsize=(15, 12))
    
    # Layout: 2x2 grid
    gs = plt.GridSpec(2, 2, figure=fig)
    
    # Panel 1: Qualia Field
    ax1 = fig.add_subplot(gs[0, 0])
    field.visualize(ax=ax1, show=False, title="Qualia Field χ(x,t)")
    
    # Panel 2: Persistence Diagram
    ax2 = fig.add_subplot(gs[0, 1])
    plot_persistence_diagram(persistence_result['diagrams'], 
                           title=f"Persistence Diagram (β₀={betti_numbers[0]}, β₁={betti_numbers[1]}, β₂={betti_numbers[2]})", 
                           ax=ax2)
    
    # Panel 3: Joy Field
    ax3 = fig.add_subplot(gs[1, 0])
    im = ax3.imshow(joy_field, cmap='RdBu_r', origin='lower')
    plt.colorbar(im, ax=ax3, label='Joy (-Ric)')
    ax3.set_title("Joy Field (Negative Ricci Curvature)")
    
    # Panel 4: Attractor Landscape
    ax4 = fig.add_subplot(gs[1, 1])
    plot_attractor_landscape(final_field, attractor_result, ax=ax4)
    
    # Add overall title with motif information
    motif_text = ""
    if motifs_result['motifs']:
        motif_text = f"Detected Motif: {motifs_result['motifs'][0]['name']} - {motifs_result['motifs'][0]['description']}"
    
    fig.suptitle(f"Topological Analysis of Qualia Field\n{motif_text}", fontsize=16)
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    output_file = os.path.join("output", "combined_topology_analysis.png")
    plt.savefig(output_file)
    plt.close(fig)
    print(f"✓ Saved combined analysis to {output_file}")
    
    print("\nTopology analysis completed successfully!")
    print("Check the 'output' directory for visualization results.")
    print("\nThis implementation demonstrates the 𝓈-Layer of ASTRA, which analyzes:")
    print("- Persistent homology (Betti numbers, persistence diagrams)")
    print("- Ricci curvature and joy fields")
    print("- Topological motifs and attractor types")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    traceback.print_exc()
    print("\nPlease check your implementation and dependencies.")
