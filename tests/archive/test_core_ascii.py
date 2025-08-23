"""
ASCII-safe version of test_core.py for ASTRA

Tests the core field implementation without Unicode characters
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Ensure the project root is on the Python path so the ``astra`` package can
# be imported when this file is executed directly.  ``__file__`` points to
# ``tests/archive/test_core_ascii.py`` so we need to traverse three directories
# up to reach the repository root.
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# Import ASTRA core modules
try:
    from astra.core import QualiaField, evolve_step, evolve_chart
    print("[PASS] Successfully imported ASTRA core modules")
except ImportError as e:
    print(f"[ERROR] Failed to import ASTRA core modules: {e}")
    sys.exit(1)

print("Testing ASTRA core functionality...")

# Create output directory if it doesn't exist
os.makedirs("output", exist_ok=True)

# Create a mock natal data object similar to the original test_core.py
class MockNatalData:
    def __init__(self):
        self.name = "Test Subject"
        
        # Mock planets with positions
        self.sun = {'abs_pos': 283.89, 'pos': 13.89, 'sign': 'Cap', 'house': '1st House', 'retrograde': False}
        self.moon = {'abs_pos': 342.00, 'pos': 12.00, 'sign': 'Pis', 'house': '2nd House', 'retrograde': False}
        self.mercury = {'abs_pos': 270.18, 'pos': 0.18, 'sign': 'Cap', 'house': '1st House', 'retrograde': False}
        self.venus = {'abs_pos': 264.33, 'pos': 24.33, 'sign': 'Sag', 'house': '12th House', 'retrograde': False}
        self.mars = {'abs_pos': 347.56, 'pos': 17.56, 'sign': 'Pis', 'house': '3rd House', 'retrograde': False}
        self.jupiter = {'abs_pos': 270.26, 'pos': 0.26, 'sign': 'Cap', 'house': '1st House', 'retrograde': False}
        self.saturn = {'abs_pos': 233.69, 'pos': 23.69, 'sign': 'Sco', 'house': '11th House', 'retrograde': True}
        self.uranus = {'abs_pos': 255.64, 'pos': 15.64, 'sign': 'Sag', 'house': '12th House', 'retrograde': False}
        self.neptune = {'abs_pos': 272.05, 'pos': 2.05, 'sign': 'Cap', 'house': '1st House', 'retrograde': False}
        self.pluto = {'abs_pos': 214.40, 'pos': 4.40, 'sign': 'Sco', 'house': '11th House', 'retrograde': True}
        
        # Mock houses
        self.first_house = {'abs_pos': 278.19, 'pos': 8.19, 'sign': 'Cap'}
        
        # These are the planets that will be accessed
        self.planets = [
            self.sun, self.moon, self.mercury, self.venus, self.mars,
            self.jupiter, self.saturn, self.uranus, self.neptune, self.pluto
        ]

# Create mock natal data
print("Creating mock natal data...")
mock_natal = MockNatalData()
print("[PASS] Created mock natal data")

# Create a QualiaField
print("Creating QualiaField...")
field = QualiaField(mock_natal, grid_size=(64, 64))
print(f"[PASS] Created QualiaField with shape {field.grid.shape}")

# Display field properties
print(f"Field min: {field.grid.min()}")
print(f"Field max: {field.grid.max()}")
print(f"Field mean: {field.grid.mean()}")

# Create visualization
print("Creating visualization...")
plt.figure(figsize=(8, 8))
plt.imshow(field.grid, cmap='viridis')
plt.colorbar(label='Field Value')
plt.title('ASTRA Qualia Field')
plt.savefig("output/qualia_field_core.png")
plt.close()
print("[PASS] Visualization saved to output/qualia_field_core.png")

# Test evolve_step function
print("Testing evolution step...")
params = {'alpha': 0.5, 'beta': 1.0, 'gamma': 0.3, 'dt': 0.01}
new_field, _ = evolve_step(field.grid, **params)
print(f"[PASS] Evolution step succeeded. New field shape: {new_field.shape}")

print("All tests passed!")
