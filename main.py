from kerykeion import AstrologicalSubject
import numpy as np
import matplotlib.pyplot as plt
import json
import os
import sys

# Import our ASTRA components
from astra.core import QualiaField, evolve_chart, visualize_evolution

# --- User Configuration ---
GEONAMES_USERNAME = "k10r"  # Your GeoNames username

# --- Natal Data ---
# Jan 4, 1985, 5:00 AM, Minneapolis, MN, USA
natal_data = {
    "name": "Test Subject",
    "year": 1985,
    "month": 1,
    "day": 4,
    "hour": 5,
    "minute": 0,
    "city": "Minneapolis",
    "nation": "US"
}

# --- Function to Print Report ---
def print_detailed_report(subject):
    print("\n" + "="*40)
    print(f"DETAILED NATAL REPORT for: {subject.name}")
    print(f"Birth Date: {subject.birth_date.strftime('%Y-%m-%d %H:%M:%S %Z%z')}")
    print(f"Location: {subject.city}, {subject.nation}")
    print("="*40 + "\n")

    print("--- Planets ---")
    # Use subject.planets_sign_long which provides full sign names
    planets_long_sign = subject.planets_sign_long
    for planet in subject.planets:
        p_name = planet['name']
        p_pos = planet['pos']
        p_sign = planets_long_sign.get(p_name, planet['sign']) # Get long name if available
        p_emoji = planet['emoji']
        p_house = planet['house']
        p_retro = " (R)" if planet['retrograde'] else ""
        print(f"- {p_name:<15} {p_pos:>6.2f}° {p_sign:<12} {p_emoji} {p_house:<10}{p_retro}")

    print("\n--- Houses (Cusps) ---")
    houses_long_sign = subject.houses_sign_long
    for i, house in enumerate(subject.houses):
        h_name = house['name']
        h_pos = house['pos']
        h_sign = houses_long_sign.get(h_name, house['sign']) # Get long name if available
        h_emoji = house['emoji']
        label = f"House {i+1}"
        if i == 0:
            label = "Ascendant (AC)"
        elif i == 3:
            label = "IC"
        elif i == 6:
            label = "Descendant (DC)"
        elif i == 9:
            label = "Midheaven (MC)"
        print(f"- {label:<15} {h_pos:>6.2f}° {h_sign:<12} {h_emoji}")

    print("\n--- Major Aspects ---")
    # Filter for major aspects (e.g., orb <= 5 for major, maybe more for Sun/Moon? Kerykeion default orbs are usually reasonable)
    # Aspect names: 'conjunction', 'opposition', 'trine', 'square', 'sextile'
    major_aspect_types = ['conjunction', 'opposition', 'trine', 'square', 'sextile']
    aspect_symbols = {
        'conjunction': '☌',
        'opposition': '☍',
        'trine': '△',
        'square': '□',
        'sextile': '∗'
    }

    # Kerykeion stores aspects in subject.aspects
    for aspect in subject.aspects:
        aspect_name = aspect['aspect'].lower()
        if aspect_name in major_aspect_types:
            p1_name = aspect['p1_name']
            p2_name = aspect['p2_name']
            orb = aspect['orb']
            aspect_symbol = aspect_symbols.get(aspect_name, '?')
            print(f"- {p1_name:<10} {aspect_symbol} {p2_name:<10} ({aspect_name.capitalize()}, Orb: {orb:.2f}°)")

    print("\n" + "="*40)
    print("End of Report")
    print("="*40 + "\n")

# --- ASTRA Testing --- 
def test_astra_core(subject):
    """Test the ASTRA core components with the birth chart"""
    
    print("\n" + "="*50)
    print("ASTRA CORE TEST - χ-LAYER INITIALIZATION & EVOLUTION")
    print("="*50)
    
    # Initialize QualiaField from chart
    print("\n[1] Initializing QualiaField from natal chart...")
    qualia_field = QualiaField(subject, grid_size=(128, 128))
    
    # Save initial field state to file
    print("\n[2] Saving initial field state visualization...")
    fig, ax = plt.subplots(figsize=(10, 8))
    qualia_field.visualize(ax=ax, show=False, title=f"Initial QualiaField for {subject.name} (t=0)")
    initial_field_file = "initial_field.png"
    plt.savefig(initial_field_file)
    plt.close(fig)
    print(f"    Saved to {initial_field_file}")
    
    # Evolve field
    print("\n[3] Evolving field for 2.0 time units...")
    field_history, time_points = evolve_chart(qualia_field, duration=2.0, dt=0.01, store_frames=5)
    
    # Save evolution visualization to file
    print("\n[4] Saving field evolution visualization...")
    plt.figure(figsize=(15, 10))
    
    # Create a custom visualization instead of using visualize_evolution
    n_frames = len(field_history)
    cols = min(3, n_frames)
    rows = (n_frames + cols - 1) // cols
    
    fig, axes = plt.subplots(rows, cols, figsize=(15, 10))
    if rows == 1 and cols == 1:
        axes = np.array([axes])  # Handle single subplot case
    axes = axes.flatten()
    
    # Determine global color scale
    vmin = min(np.min(f) for f in field_history)
    vmax = max(np.max(f) for f in field_history)
    
    # Plot each frame
    for i, (field, t) in enumerate(zip(field_history, time_points)):
        if i < len(axes):
            im = axes[i].imshow(field, origin='lower', cmap='viridis', 
                              interpolation='nearest', vmin=vmin, vmax=vmax)
            axes[i].set_title(f"t = {t:.2f}")
            axes[i].set_xticks([])
            axes[i].set_yticks([])
    
    # Hide unused subplots
    for i in range(n_frames, len(axes)):
        axes[i].axis('off')
    
    # Add colorbar
    fig.subplots_adjust(right=0.9)
    cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
    fig.colorbar(im, cax=cbar_ax, label='χ(x,t) magnitude')
    
    # Add overall title
    fig.suptitle(f"QualiaField Evolution for {subject.name}", fontsize=16)
    plt.tight_layout(rect=[0, 0, 0.9, 0.95])
    
    # Save to file
    evolution_file = "field_evolution.png"
    plt.savefig(evolution_file)
    plt.close(fig)
    print(f"    Saved to {evolution_file}")
    
    print("\nℹ️ The evolved field represents your psychological/archetypal state space")
    print("This is the foundational χ-Layer in ASTRA's architecture.")
    print("Future versions will add the 𝒸-Layer (planetary operators) and")
    print("𝓈-Layer (topological analysis) on top of this baseline evolution.")
    
    return qualia_field, field_history, time_points

# --- Run Tests Function ---
def run_tests():
    """Run the ASTRA diagnostic and component tests"""
    print("\n" + "="*50)
    print("ASTRA TESTING SUITE")
    print("="*50)
    
    # Create output directory if it doesn't exist
    os.makedirs("output/diagnostic", exist_ok=True)
    
    tests_available = [
        ("Diagnostic Test", "tests/test_diagnostic.py"),
        ("Core Test", "tests/test_core.py"),
        ("Evolution Test", "tests/test_evolution.py"),
        ("Topology Test", "tests/test_topology.py"),
        ("Narrative Test", "tests/test_narrative.py"),
        ("Simple Test", "tests/test_simple.py")
    ]
    
    for i, (test_name, test_path) in enumerate(tests_available):
        test_exists = os.path.exists(test_path)
        print(f"{i+1}. {test_name}: {'✅ Available' if test_exists else '❌ Not found'} - {test_path}")
    
    print("\nTo run a specific test, use: python <test_file>")
    print("For comprehensive diagnostics, run: python tests/test_diagnostic.py")
    print("="*50)

# --- Main Execution ---
if __name__ == "__main__":
    # Check if we're running a specific command
    args = sys.argv[1:]
    if len(args) > 0 and args[0] == "--test":
        run_tests()
        sys.exit(0)
        
    print(f"Attempting to create chart for: {natal_data['name']}")
    print(f"Birth Date: {natal_data['month']}/{natal_data['day']}/{natal_data['year']}")
    print(f"Birth Time: {natal_data['hour']:02d}:{natal_data['minute']:02d}")
    print(f"Birth Location: {natal_data['city']}, {natal_data['nation']}")
    print("-" * 30)

    try:
        # Create the AstrologicalSubject instance
        subject = AstrologicalSubject(
            natal_data["name"],
            natal_data["year"],
            natal_data["month"],
            natal_data["day"],
            natal_data["hour"],
            natal_data["minute"],
            natal_data["city"],
            natal_data["nation"]
        )

        print("Successfully created Kerykeion AstrologicalSubject!")
        print("-" * 30)

        # Print the detailed natal report
        print_detailed_report(subject)
        
        # Test ASTRA Core
        qualia_field, field_history, time_points = test_astra_core(subject)
        
        print("\nASTRA Test Complete!")

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        print("Please check your input data and internet connection.")
        print("Ensure you have installed the necessary libraries: pip install -r requirements.txt")
        
        print("\nYou can also run the tests to verify ASTRA components:")
        print("  python main.py --test")
