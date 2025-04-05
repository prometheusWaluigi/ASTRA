"""
Test module for ASTRA core functionality

Tests the basic QualiaField initialization and properties
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Add the parent directory to the path so we can import astra
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Output directory setup
os.makedirs("output/tests", exist_ok=True)

def test_qualia_field():
    """Test QualiaField initialization and basic properties"""
    from astra.core import QualiaField
    
    # Create a simplified mock natal data object
    class SimpleMockNatal:
        def __init__(self):
            self.name = "Test Subject"
            self.planets = []
                
            # Add required basic planets
            self.sun = {'abs_pos': 283.89, 'pos': 13.89, 'sign': 'Cap', 'house': '1st House'}
            self.moon = {'abs_pos': 342.00, 'pos': 12.00, 'sign': 'Pis', 'house': '2nd House'}
            
            # Add first house information
            self.first_house = {'abs_pos': 278.19, 'pos': 8.19, 'sign': 'Cap'}
            
            # Add additional planets that might be used
            self.mercury = {'abs_pos': 270.18, 'pos': 0.18, 'sign': 'Cap', 'house': '1st House'}
            self.venus = {'abs_pos': 264.33, 'pos': 24.33, 'sign': 'Sag', 'house': '12th House'}
            self.mars = {'abs_pos': 347.56, 'pos': 17.56, 'sign': 'Pis', 'house': '3rd House'}
            self.jupiter = {'abs_pos': 270.26, 'pos': 0.26, 'sign': 'Cap', 'house': '1st House'}
            self.saturn = {'abs_pos': 233.69, 'pos': 23.69, 'sign': 'Sco', 'house': '11th House'}
            self.uranus = {'abs_pos': 255.64, 'pos': 15.64, 'sign': 'Sag', 'house': '12th House'}
            self.neptune = {'abs_pos': 272.05, 'pos': 2.05, 'sign': 'Cap', 'house': '1st House'}
            self.pluto = {'abs_pos': 214.40, 'pos': 4.40, 'sign': 'Sco', 'house': '11th House'}
    
    # Initialize QualiaField
    print("Creating mock natal data...")
    mock_natal = SimpleMockNatal()
    print("Creating QualiaField...")
    field = QualiaField(mock_natal, grid_size=(64, 64))
    
    # Get field state
    try:
        if hasattr(field, 'state'):
            field_state = field.state
            print(f"Field state shape: {field_state.shape}")
        elif hasattr(field, 'grid'):
            field_state = field.grid
            print(f"Field grid shape: {field_state.shape}")
        else:
            print("Could not access field state or grid")
            return False
    except Exception as e:
        print(f"Error accessing field state: {e}")
        return False
    
    # Check field properties
    if hasattr(field, 'params'):
        print("Field parameters:")
        for key, value in field.params.items():
            print(f"  {key}: {value}")
    
    # Save a visualization of the field
    try:
        plt.figure(figsize=(8, 8))
        plt.imshow(field_state, cmap='viridis')
        plt.colorbar(label='Field Value')
        plt.title('ASTRA Qualia Field')
        plt.savefig("output/tests/qualia_field_test.png")
        plt.close()
        print("Field visualization saved to output/tests/qualia_field_test.png")
    except Exception as e:
        print(f"Error creating visualization: {e}")
    
    return True

if __name__ == "__main__":
    print(f"Running core tests at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        success = test_qualia_field()
        if success:
            print("CORE TESTS PASSED")
            sys.exit(0)
        else:
            print("CORE TESTS FAILED")
            sys.exit(1)
    except Exception as e:
        print(f"Error in core tests: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
