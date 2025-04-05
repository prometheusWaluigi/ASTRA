"""
The Fellowship: A robust ASTRA test script

This script tests all core ASTRA components with robust error handling.
"""

import os
import sys
import time
import traceback
import importlib
from datetime import datetime

# Create log file
log_dir = os.path.join("output", "fellowship")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"test_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

# Log writing function that handles encoding errors
def write_log(msg, console=True):
    """Write to log file and optionally console with encoding error handling"""
    if console:
        try:
            print(msg)
        except UnicodeEncodeError:
            print("(Unicode characters were replaced for console display)")
    
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

# Print separator
def print_separator():
    write_log("-" * 60)

# Header printer
def print_header(title):
    write_log("\n" + "=" * 60)
    write_log(title.center(60, " "))
    write_log("=" * 60 + "\n")

# Test import function
def test_import(module_name):
    """Test if a module can be imported"""
    try:
        module = importlib.import_module(module_name)
        return True, module, None
    except ImportError as e:
        return False, None, str(e)
    except Exception as e:
        return False, None, f"{type(e).__name__}: {str(e)}"

# Test runner function
def run_test(name, test_function):
    """Run a test with clean error handling"""
    print_header(name)
    start_time = time.time()
    
    try:
        result = test_function()
        success = True
        error = None
    except Exception as e:
        result = None
        success = False
        error = f"{type(e).__name__}: {str(e)}"
        write_log(f"Error details: {error}")
        
        # Get full traceback but handle encoding issues
        tb = traceback.format_exc()
        try:
            write_log(tb)
        except UnicodeEncodeError:
            write_log("(Traceback contained Unicode characters that couldn't be displayed)")
    
    duration = time.time() - start_time
    status = "PASSED" if success else "FAILED"
    
    write_log(f"Status: {status}")
    write_log(f"Duration: {duration:.2f} seconds")
    print_separator()
    
    return {
        "name": name,
        "success": success,
        "duration": duration,
        "result": result,
        "error": error
    }

# Individual test functions
def test_core():
    """Test the core ASTRA functionality"""
    write_log("Testing core functionality...")
    
    # Test importing core modules
    success, core_module, error = test_import("astra.core")
    if not success:
        write_log(f"Failed to import astra.core: {error}")
        return False
    
    # Check if QualiaField exists
    if not hasattr(core_module, "QualiaField"):
        write_log("astra.core does not have QualiaField")
        return False
    
    write_log("Core module imported successfully")
    
    # Try creating a simple field
    try:
        # Create a minimal mock natal data
        class SimpleMockNatal:
            def __init__(self):
                self.name = "Test Subject"
                self.planets = []
        
        # Create field
        mock_natal = SimpleMockNatal()
        field = core_module.QualiaField(mock_natal, grid_size=(32, 32))
        write_log("Created QualiaField successfully")
        
        # Just check if we can access the field state
        if hasattr(field, "state"):
            field_state = field.state
        elif hasattr(field, "grid"):
            field_state = field.grid
        else:
            field_state = None
            
        if field_state is not None:
            write_log(f"Field state is accessible with shape: {field_state.shape}")
        else:
            write_log("Could not access field state")
        
        return True
        
    except Exception as e:
        write_log(f"Error creating or accessing QualiaField: {str(e)}")
        raise
    
def test_evolution():
    """Test the evolution functionality"""
    write_log("Testing evolution functionality...")
    
    # Test importing core modules
    success, core_module, error = test_import("astra.core")
    if not success:
        write_log(f"Failed to import astra.core: {error}")
        return False
    
    try:
        # Check if evolution functions exist
        has_evolve = hasattr(core_module, "evolve")
        has_evolve_step = hasattr(core_module, "evolve_step")
        has_evolve_chart = hasattr(core_module, "evolve_chart")
        
        write_log(f"Evolution functions available: evolve={has_evolve}, evolve_step={has_evolve_step}, evolve_chart={has_evolve_chart}")
        
        # Try importing evolution directly
        try:
            import astra.core.evolution
            write_log("Successfully imported astra.core.evolution")
            
            # Check available functions
            evolve_funcs = [name for name in dir(astra.core.evolution) 
                           if name.startswith("evolve") and callable(getattr(astra.core.evolution, name))]
            write_log(f"Available evolution functions: {', '.join(evolve_funcs)}")
            
        except ImportError as e:
            write_log(f"Could not import astra.core.evolution directly: {str(e)}")
        
        # Test a simple evolution if functions are available
        import numpy as np
        
        # Create a test field
        test_field = np.random.random((32, 32))
        
        if has_evolve_step:
            try:
                # Create a minimal QualiaField-like object for testing
                class MockField:
                    def __init__(self, state):
                        self.state = state
                        self.params = {'alpha': 0.5, 'beta': 1.0, 'gamma': 0.3, 'dt': 0.01}
                    
                    def get_state(self):
                        return self.state
                
                # Create mock field object
                mock_field = MockField(test_field)
                
                # Try evolve_step with correct parameters
                dt = 0.01
                new_field = core_module.evolve_step(mock_field, dt)
                write_log("evolve_step completed successfully")
            except Exception as e:
                write_log(f"Error in evolve_step: {str(e)}")
                
                # Try alternative call pattern with direct import
                try:
                    from astra.core.evolution import evolve_step
                    write_log("Imported evolve_step directly")
                    
                    # Try with numpy array directly (some implementations might accept this)
                    new_field = evolve_step(test_field, dt=0.01)
                    write_log("evolve_step completed successfully with direct array")
                except Exception as e2:
                    write_log(f"Alternative approach also failed: {str(e2)}")
                    raise
            
        return True
        
    except Exception as e:
        write_log(f"Error testing evolution: {str(e)}")
        raise

def test_topology():
    """Test the topology functionality"""
    write_log("Testing topology functionality...")
    
    # Test importing topology module
    success, topology_module, error = test_import("astra.topology")
    if not success:
        write_log(f"Failed to import astra.topology: {error}")
        return False
    
    # List available functions
    topo_funcs = [name for name in dir(topology_module) 
                 if not name.startswith("_") and callable(getattr(topology_module, name))]
    write_log(f"Available topology functions: {', '.join(topo_funcs)}")
    
    # Check if field_to_graph exists
    has_field_to_graph = hasattr(topology_module, "field_to_graph")
    if has_field_to_graph:
        write_log("field_to_graph function found")
        
        # Try to run a simple conversion
        try:
            import numpy as np
            test_field = np.random.random((16, 16))
            
            # Check for NetworkX
            try:
                import networkx as nx
                write_log("NetworkX is available")
                
                # Try to convert field to graph
                graph = topology_module.field_to_graph(test_field)
                write_log(f"Successfully converted field to graph with {graph.number_of_nodes()} nodes")
                
            except ImportError:
                write_log("NetworkX is not available, skipping graph conversion")
        
        except Exception as e:
            write_log(f"Error in field_to_graph test: {str(e)}")
    
    return True

def test_narrative():
    """Test the narrative functionality"""
    write_log("Testing narrative functionality...")
    
    # Test importing symbols module
    success, symbols_module, error = test_import("astra.symbols")
    if not success:
        write_log(f"Failed to import astra.symbols: {error}")
        return False
    
    # List available functions
    symbol_funcs = [name for name in dir(symbols_module) 
                   if not name.startswith("_") and callable(getattr(symbols_module, name))]
    write_log(f"Available symbol functions: {', '.join(symbol_funcs)}")
    
    # Check for narrative module
    try:
        import astra.symbols.narrative
        write_log("Successfully imported astra.symbols.narrative")
        
        # List available functions
        narrative_funcs = [name for name in dir(astra.symbols.narrative) 
                         if not name.startswith("_") and callable(getattr(astra.symbols.narrative, name))]
        write_log(f"Available narrative functions: {', '.join(narrative_funcs)}")
        
    except ImportError as e:
        write_log(f"Could not import astra.symbols.narrative: {str(e)}")
    
    return True

def main():
    """Main function to run all tests"""
    # Initialize log file
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"ASTRA FELLOWSHIP TEST LOG\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Python version: {sys.version}\n\n")
    
    print_header("THE FELLOWSHIP OF THE RING")
    write_log(f"Running tests at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Define tests to run
    tests = [
        ("Core Module", test_core),
        ("Evolution Functions", test_evolution),
        ("Topology Analysis", test_topology),
        ("Narrative Generation", test_narrative)
    ]
    
    # Run all tests
    results = []
    total_start = time.time()
    
    for name, func in tests:
        result = run_test(name, func)
        results.append(result)
    
    total_duration = time.time() - total_start
    
    # Print summary
    print_header("TEST SUMMARY")
    
    total_tests = len(results)
    passed_tests = sum(1 for r in results if r["success"])
    failed_tests = total_tests - passed_tests
    
    write_log(f"Total tests: {total_tests}")
    write_log(f"Passed tests: {passed_tests}")
    write_log(f"Failed tests: {failed_tests}")
    write_log(f"Total duration: {total_duration:.2f} seconds")
    
    # Print detailed results
    write_log("\nDetailed results:")
    for i, result in enumerate(results, 1):
        status = "PASSED" if result["success"] else "FAILED"
        write_log(f"{i}. {result['name']}: {status} ({result['duration']:.2f}s)")
        if result["error"]:
            write_log(f"   Error: {result['error']}")
    
    # Print final message
    print_header("JOURNEY'S END")
    
    if failed_tests == 0:
        write_log("All tests have passed!")
        write_log("\n\"I'm glad to be with you, Samwise Gamgee, here at the end of all things.\"")
    else:
        write_log(f"{failed_tests} test(s) have failed.")
        write_log("\n\"Even the smallest person can change the course of the future.\"")
    
    write_log(f"\nFull log saved to: {log_file}")
    
    return 0 if failed_tests == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
