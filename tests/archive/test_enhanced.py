"""
Enhanced test script for the ASTRA core functionality with the full fKPZχ equation.

This script demonstrates the enhanced implementation of the fractal Kardar-Parisi-Zhang-χ 
equation for consciousness modeling:

∂_t χ(x,t) = ν ∇^α χ(x,t) + (λ/2)(∇^β χ(x,t))^2 + η_f(x,t) + γ B[χ]

This includes:
- Fractional Laplacian for long-range coherence
- Nonlinear term for recursive amplification
- Fractal noise for cognitive perturbations
- Symmetry breaking term for ego formation
- Joy as negative Ricci curvature
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

print("Testing ASTRA enhanced fKPZχ implementation...")

try:
    # Import ASTRA core components
    from astra.core.field import QualiaField
    from astra.core.evolution_enhanced import (
        evolve_chart_enhanced, 
        visualize_evolution_enhanced,
        meditation_lambda_damping,
        compute_joy
    )
    print("✓ Successfully imported ASTRA enhanced modules")
    
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
    output_file = os.path.join("output", "enhanced_initial_field.png")
    plt.savefig(output_file)
    plt.close(fig)
    print(f"✓ Saved to {output_file}")
    
    # Evolve the field with normal consciousness state
    print("\nEvolving field in normal consciousness state...")
    result_normal = evolve_chart_enhanced(
        field, 
        duration=0.5, 
        params=enhanced_params, 
        store_frames=3,
        compute_metrics=True
    )
    print(f"✓ Field evolved in normal state")
    
    # Save normal evolution visualization
    fig = visualize_evolution_enhanced(
        result_normal,
        title="Normal Consciousness State",
        show_metrics=True
    )
    output_file = os.path.join("output", "enhanced_normal_evolution.png")
    plt.savefig(output_file)
    plt.close(fig)
    print(f"✓ Saved to {output_file}")
    
    # Reset field to initial state
    field = QualiaField(mock_natal, grid_size=(128, 128))
    
    # Evolve with meditation state (reduced lambda)
    print("\nEvolving field in meditation state...")
    meditation_params = enhanced_params.copy()
    meditation_params['theta'] = 1.0  # High meditation state
    
    result_meditation = evolve_chart_enhanced(
        field, 
        duration=0.5, 
        params=meditation_params, 
        store_frames=3,
        compute_metrics=True
    )
    print(f"✓ Field evolved in meditation state")
    
    # Save meditation evolution visualization
    fig = visualize_evolution_enhanced(
        result_meditation,
        title="Meditation State (λ-damping)",
        show_metrics=True
    )
    output_file = os.path.join("output", "enhanced_meditation_evolution.png")
    plt.savefig(output_file)
    plt.close(fig)
    print(f"✓ Saved to {output_file}")
    
    # Compare joy metrics between normal and meditation states
    print("\nComparing joy metrics...")
    fig, ax = plt.subplots(figsize=(10, 6))
    
    normal_joy = [np.mean(joy) for joy in result_normal['metrics']['joy']]
    meditation_joy = [np.mean(joy) for joy in result_meditation['metrics']['joy']]
    
    ax.plot(result_normal['time_points'], normal_joy, 'r-o', label='Normal State')
    ax.plot(result_meditation['time_points'], meditation_joy, 'b-o', label='Meditation State')
    
    ax.set_title('Joy Comparison (-Ric)')
    ax.set_xlabel('Time')
    ax.set_ylabel('Average Joy')
    ax.legend()
    ax.grid(True)
    
    output_file = os.path.join("output", "joy_comparison.png")
    plt.savefig(output_file)
    plt.close(fig)
    print(f"✓ Saved joy comparison to {output_file}")
    
    # Compare coherence metrics
    print("\nComparing coherence metrics...")
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(result_normal['time_points'], result_normal['metrics']['coherence'], 'r-o', label='Normal State')
    ax.plot(result_meditation['time_points'], result_meditation['metrics']['coherence'], 'b-o', label='Meditation State')
    
    ax.set_title('Coherence Comparison')
    ax.set_xlabel('Time')
    ax.set_ylabel('Coherence')
    ax.legend()
    ax.grid(True)
    
    output_file = os.path.join("output", "coherence_comparison.png")
    plt.savefig(output_file)
    plt.close(fig)
    print(f"✓ Saved coherence comparison to {output_file}")
    
    print("\nEnhanced test completed successfully!")
    print("Check the 'output' directory for visualization results.")
    print("\nThis implementation demonstrates the fKPZχ equation:")
    print("∂_t χ(x,t) = ν ∇^α χ(x,t) + (λ/2)(∇^β χ(x,t))^2 + η_f(x,t) + γ B[χ]")
    print("\nWith the following key concepts:")
    print("- Fractional Laplacian for long-range coherence")
    print("- Nonlinear term for recursive amplification")
    print("- Fractal noise for cognitive perturbations")
    print("- Symmetry breaking term for ego formation")
    print("- Joy as negative Ricci curvature")
    print("- Meditation as λ-damping")

except Exception as e:
    print(f"\n❌ Error: {e}")
    traceback.print_exc()
    print("\nPlease check your implementation and dependencies.")
