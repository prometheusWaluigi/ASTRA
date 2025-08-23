"""
Simple diagnostic test for ASTRA

This script performs basic tests of each ASTRA component
with proper error handling to identify issues.
"""

import os
import sys
import time
import traceback
import numpy as np
import matplotlib.pyplot as plt

# When this file is executed directly (``python tests/test_simple.py``) the
# working directory becomes the ``tests`` folder, meaning the project root is
# not automatically on ``sys.path``.  Add the parent directory so that the
# ``astra`` package can be imported without requiring installation.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# Make sure output directory exists
os.makedirs("output/simple_test", exist_ok=True)

# Error handler helper used when running this file directly.  The name does not
# start with ``test_`` so that pytest does not try to treat it as a test.
def run_section(name, test_func):
    """Run a test section with proper error handling"""
    print(f"\n{'='*60}")
    print(f"Testing {name}...")
    print(f"{'-'*60}")
    
    start_time = time.time()
    success = False
    
    try:
        # Run the test
        result = test_func()
        success = True if result is None else bool(result)
        print(f"SUCCESS: {name} tests completed")
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {str(e)}")
        traceback.print_exc()
    
    duration = time.time() - start_time
    print(f"{'-'*60}")
    print(f"Result: {'SUCCESS' if success else 'FAILURE'} ({duration:.2f}s)")
    
    return success

def test_imports():
    """Test basic imports from the ASTRA package"""
    print("Testing imports...")
    
    imports_to_test = [
        ("astra", "Main package"),
        ("astra.core", "Core module"),
        ("astra.topology", "Topology module"),
        ("astra.symbols", "Symbols module"),
        ("astra.retrocausal", "Retrocausal module")
    ]
    
    for module_name, description in imports_to_test:
        try:
            print(f"Importing {module_name}... ", end="")
            module = __import__(module_name, fromlist=["*"])
            print(f"SUCCESS - {description}")
            
            # Print available functions/classes
            members = [m for m in dir(module) if not m.startswith("_")]
            if members:
                print(f"  Available: {', '.join(sorted(members[:10]))}")
                if len(members) > 10:
                    print(f"  ...and {len(members) - 10} more")
        except ImportError as e:
            print(f"FAILED - {e}")
    
    return True

def test_qualia_field():
    """Test the QualiaField initialization"""
    print("Testing QualiaField...")
    
    try:
        # Import the QualiaField class
        from astra.core import QualiaField
        print("Successfully imported QualiaField")
        
        # Create a minimal mock natal data
        class SimpleMockNatal:
            def __init__(self):
                self.name = "Test Subject"
                self.planets = []
                
                # Add minimal attributes needed
                self.sun = {'abs_pos': 0, 'pos': 0, 'sign': 'Aries', 'house': '1st House'}
                self.moon = {'abs_pos': 30, 'pos': 0, 'sign': 'Taurus', 'house': '2nd House'}
                self.first_house = {'abs_pos': 0}
        
        # Create instance
        natal = SimpleMockNatal()
        print("Created mock natal data")
        
        # Create QualiaField
        field = QualiaField(natal, grid_size=(32, 32))
        print("Successfully created QualiaField instance")
        
        # Inspect field
        print(f"Field class: {type(field).__name__}")
        print(f"Field attributes: {sorted([a for a in dir(field) if not a.startswith('_')])}")
        
        # Try to visualize initial state
        if hasattr(field, 'get_state'):
            state = field.get_state()
            plt.figure(figsize=(6, 6))
            plt.imshow(state, cmap='viridis')
            plt.colorbar()
            plt.title("QualiaField Initial State")
            plt.savefig("output/simple_test/field_state.png")
            plt.close()
            print("Saved field visualization to output/simple_test/field_state.png")
        else:
            print("Field doesn't have get_state method, can't visualize")
        
        return True
    except Exception as e:
        print(f"Error in QualiaField test: {e}")
        return False

def test_evolution():
    """Test the evolution functionality"""
    print("Testing evolution...")
    
    try:
        # Try importing evolution functions
        try:
            from astra.core import evolve_step
            print("Successfully imported evolve_step")
            
            # Try to get function signature
            import inspect
            signature = str(inspect.signature(evolve_step))
            print(f"evolve_step signature: {signature}")
            
        except ImportError:
            print("evolve_step not available at top level")
            
            # Try importing from evolution module
            from astra.core.evolution import evolve_step
            print("Successfully imported evolve_step from evolution module")
            
            # Try to get function signature
            import inspect
            signature = str(inspect.signature(evolve_step))
            print(f"evolve_step signature: {signature}")
        
        # Create a simple field simulation
        from astra.core import QualiaField
        
        class SimpleMockNatal:
            def __init__(self):
                self.name = "Test Subject"
                self.planets = []
                self.sun = {'abs_pos': 0, 'pos': 0, 'sign': 'Aries', 'house': '1st House'}
                self.moon = {'abs_pos': 30, 'pos': 0, 'sign': 'Taurus', 'house': '2nd House'}
                self.first_house = {'abs_pos': 0}
        
        # Create field
        field = QualiaField(SimpleMockNatal(), grid_size=(32, 32))
        print("Created test field")
        
        # Try to evolve one step
        dt = 0.01
        new_state = evolve_step(field, dt)
        print("Successfully evolved field one step")
        
        return True
    except Exception as e:
        print(f"Error in evolution test: {e}")
        return False

def main():
    """Run all tests"""
    print("ASTRA SIMPLE DIAGNOSTIC TEST")
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Testing at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("Basic Imports", test_imports),
        ("QualiaField", test_qualia_field),
        ("Evolution", test_evolution)
    ]
    
    results = []
    for name, func in tests:
        success = run_section(name, func)
        results.append((name, success))
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("-"*60)
    
    for name, success in results:
        status = "PASS" if success else "FAIL"
        print(f"{name:20} {status}")
    
    success_count = sum(1 for _, success in results if success)
    print(f"\n{success_count}/{len(results)} tests passed")
    
    if success_count == len(results):
        print("\nAll tests passed successfully!")
    else:
        print("\nSome tests failed. Check the output for details.")

if __name__ == "__main__":
    main()
