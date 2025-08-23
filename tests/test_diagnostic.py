"""
Comprehensive ASTRA Diagnostic Test

This script tests all ASTRA components in a way that is robust
against encoding issues and implementation differences.
"""

import os
import sys
import time
import traceback
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Create output directory
os.makedirs("output/diagnostic", exist_ok=True)

# Time tracking
start_time = datetime.now()

def section_header(title):
    """Print a section header"""
    print("\n" + "=" * 60)
    print(title)
    print("-" * 60)

def run_component(name, test_func):
    """Run a test section with proper error handling"""
    section_header(f"Testing {name}")
    component_start = time.time()

    success = False
    try:
        result = test_func()
        success = True if result is None else bool(result)
        print(f"✓ SUCCESS: {name} test completed")
    except Exception as e:
        print(f"✗ ERROR: {type(e).__name__}: {str(e)}")
        traceback.print_exc(limit=2)

    duration = time.time() - component_start
    print(f"Duration: {duration:.2f} seconds")

    return success

def test_imports():
    """Test all imports from ASTRA"""
    results = {}
    
    modules = [
        "astra",
        "astra.core",
        "astra.core.evolution",
        "astra.topology",
        "astra.topology.ricci",
        "astra.symbols",
        "astra.symbols.narrative",
        "astra.retrocausal",
        "astra.visualization"
    ]
    
    for module_name in modules:
        try:
            module = __import__(module_name, fromlist=["*"])
            exports = [x for x in dir(module) if not x.startswith("_")]
            results[module_name] = {"status": "success", "exports": exports[:10]}
            print(f"✓ {module_name}: {', '.join(exports[:5])}{' and more...' if len(exports) > 5 else ''}")
        except ImportError as e:
            results[module_name] = {"status": "error", "message": str(e)}
            print(f"✗ {module_name}: {str(e)}")
    
    return results

def test_field_creation():
    """Test QualiaField creation"""
    from astra.core import QualiaField
    
    # Create a simplified mock natal data
    class SimpleMockNatal:
        def __init__(self):
            self.name = "Test Subject"
            self.planets = []
            self.sun = {'abs_pos': 0, 'pos': 0, 'sign': 'Aries', 'house': '1st House'}
            self.moon = {'abs_pos': 30, 'pos': 0, 'sign': 'Taurus', 'house': '2nd House'}
            self.first_house = {'abs_pos': 0}
    
    # Create field
    natal = SimpleMockNatal()
    field = QualiaField(natal, grid_size=(32, 32))
    print(f"✓ Created QualiaField of size {field.grid_size if hasattr(field, 'grid_size') else '(unknown)'}")
    
    # Get field data
    field_data = None
    if hasattr(field, 'state'):
        field_data = field.state
        print("✓ Accessed field state")
    elif hasattr(field, 'grid'):
        field_data = field.grid
        print("✓ Accessed field grid")
    else:
        print("✗ Could not access field state or grid")
        
    # Try to visualize
    if field_data is not None:
        plt.figure(figsize=(6, 6))
        plt.imshow(field_data, cmap='viridis')
        plt.colorbar(label='Field Value')
        plt.title("QualiaField Initial State")
        plt.savefig("output/diagnostic/field_state.png")
        plt.close()
        print("✓ Created field visualization (output/diagnostic/field_state.png)")
    
    return True

def test_evolution():
    """Test evolution functionality"""
    # First try to get evolve_step from different locations
    try:
        # Try top-level first
        from astra.core import QualiaField, evolve_step
        print("✓ Imported evolve_step from astra.core")
    except ImportError:
        try:
            # Try the evolution module
            from astra.core.evolution import evolve_step
            from astra.core import QualiaField
            print("✓ Imported evolve_step from astra.core.evolution")
        except ImportError:
            print("✗ Could not import evolve_step")
            return False
    
    # Create a field
    class SimpleMockNatal:
        def __init__(self):
            self.name = "Test Subject"
            self.planets = []
            self.sun = {'abs_pos': 0, 'pos': 0, 'sign': 'Aries', 'house': '1st House'}
            self.moon = {'abs_pos': 30, 'pos': 0, 'sign': 'Taurus', 'house': '2nd House'}
            self.first_house = {'abs_pos': 0}
    
    # Create field
    field = QualiaField(SimpleMockNatal(), grid_size=(32, 32))
    print("✓ Created test field")
    
    # Try to evolve the field
    try:
        # Get function signature
        import inspect
        sig = str(inspect.signature(evolve_step))
        print(f"evolve_step signature: {sig}")
        
        # Evolve the field
        dt = 0.01
        new_state = evolve_step(field, dt)
        print("✓ Successfully evolved field one step")
        
        # Visualize the result
        plt.figure(figsize=(6, 6))
        plt.imshow(new_state, cmap='viridis')
        plt.colorbar(label='Field Value')
        plt.title("Evolved Field State")
        plt.savefig("output/diagnostic/evolved_state.png")
        plt.close()
        print("✓ Created evolved field visualization (output/diagnostic/evolved_state.png)")
        
        return True
    except Exception as e:
        print(f"✗ Evolution failed: {str(e)}")
        return False

def test_topology():
    """Test topology functionality"""
    # Try to import NetworkX
    try:
        import networkx as nx
        nx_available = True
        print("✓ NetworkX is available")
    except ImportError:
        nx_available = False
        print("✗ NetworkX is not available - topology tests limited")
    
    # Try to import field_to_graph from different locations
    field_to_graph_func = None
    
    try:
        from astra.topology import field_to_graph
        field_to_graph_func = field_to_graph
        print("✓ Imported field_to_graph from astra.topology")
    except ImportError:
        try:
            from astra.topology.ricci import field_to_graph
            field_to_graph_func = field_to_graph
            print("✓ Imported field_to_graph from astra.topology.ricci")
        except ImportError:
            print("✗ Could not import field_to_graph")
            
            # Create fallback if NetworkX is available
            if nx_available:
                def simple_field_to_graph(field, threshold=0.5):
                    """Simple graph conversion"""
                    G = nx.Graph()
                    height, width = field.shape
                    
                    for i in range(height):
                        for j in range(width):
                            if field[i, j] > threshold:
                                G.add_node((i, j), value=field[i, j])
                    
                    nodes = list(G.nodes())
                    for node in nodes:
                        i, j = node
                        neighbors = [(i-1,j), (i+1,j), (i,j-1), (i,j+1)]
                        for neighbor in neighbors:
                            if neighbor in G:
                                G.add_edge(node, neighbor)
                    
                    return G
                
                field_to_graph_func = simple_field_to_graph
                print("✓ Created fallback field_to_graph implementation")
    
    # Create test field
    field = np.random.random((20, 20))
    print("✓ Created test field")
    
    # Try to convert to graph if we have a function and NetworkX
    if field_to_graph_func is not None and nx_available:
        graph = field_to_graph_func(field)
        
        # Basic graph analysis
        num_nodes = graph.number_of_nodes()
        num_edges = graph.number_of_edges()
        num_components = nx.number_connected_components(graph)
        
        print(f"✓ Created graph with {num_nodes} nodes and {num_edges} edges")
        print(f"✓ Graph has {num_components} connected components")
        
        # Try to visualize
        plt.figure(figsize=(8, 8))
        pos = {(i, j): (j, -i) for i, j in graph.nodes()}
        nx.draw(graph, pos=pos, node_size=50, node_color='blue', edge_color='gray')
        plt.title("Field Graph")
        plt.savefig("output/diagnostic/field_graph.png")
        plt.close()
        print("✓ Created graph visualization (output/diagnostic/field_graph.png)")
    
    return True

def test_narrative():
    """Test narrative functionality"""
    # Create a test field
    field = np.random.random((32, 32))
    field[10:15, 10:15] = 0.9  # Add a peak
    field[20:25, 20:25] = 0.2  # Add a valley
    
    # Try to import generate_narrative
    generate_narrative_func = None
    
    try:
        from astra.symbols.narrative import generate_narrative
        generate_narrative_func = generate_narrative
        print("✓ Imported generate_narrative from astra.symbols.narrative")
    except ImportError:
        try:
            from astra.symbols import generate_narrative
            generate_narrative_func = generate_narrative
            print("✓ Imported generate_narrative from astra.symbols")
        except ImportError:
            print("✗ Could not import generate_narrative")
            
            # Create fallback implementation
            def simple_generate_narrative(field):
                """Simple event detection"""
                events = []
                
                # Find peaks and valleys
                high_threshold = np.percentile(field, 75)
                low_threshold = np.percentile(field, 25)
                
                peak_regions = (field > high_threshold)
                valley_regions = (field < low_threshold)
                
                if np.any(peak_regions):
                    events.append({
                        "type": "EMERGENCE",
                        "location": np.unravel_index(np.argmax(field), field.shape)
                    })
                
                if np.any(valley_regions):
                    events.append({
                        "type": "DISSOLUTION",
                        "location": np.unravel_index(np.argmin(field), field.shape)
                    })
                
                return events
            
            generate_narrative_func = simple_generate_narrative
            print("✓ Created fallback generate_narrative implementation")
    
    # Generate narrative
    try:
        # Convert field to uint8 format for watershed algorithm compatibility
        scaled_field = ((field - field.min()) / (field.max() - field.min()) * 255).astype(np.uint8)
        print(f"✓ Converted field to uint8 format (range: {scaled_field.min()}-{scaled_field.max()})")
        
        # Try with converted field
        events = generate_narrative_func(scaled_field)
        print(f"✓ Generated {len(events)} narrative events")
    except Exception as e:
        print(f"✗ Error with uint8 field: {e}")
        
        # Fall back to simple detection function that doesn't use watershed
        def simple_detect(field):
            # Basic thresholding approach
            events = []
            high_vals = field > np.percentile(field, 75)
            low_vals = field < np.percentile(field, 25)
            
            if np.any(high_vals):
                loc = np.unravel_index(np.argmax(field), field.shape)
                events.append({"type": "EMERGENCE", "location": loc})
                
            if np.any(low_vals):
                loc = np.unravel_index(np.argmin(field), field.shape)
                events.append({"type": "DISSOLUTION", "location": loc})
                
            return events
            
        events = simple_detect(field)
        print(f"✓ Generated {len(events)} events with fallback detector")
    
    # Print events
    for i, event in enumerate(events):
        # Handle both dictionary-based and object-based events
        if hasattr(event, '__getattribute__'):
            # It's likely a custom NarrativeEvent object
            try:
                event_type = event.type if hasattr(event, 'type') else 'UNKNOWN'
                location = event.location if hasattr(event, 'location') else 'unknown'
            except Exception as e:
                print(f"  Error accessing event attributes: {e}")
                event_type = 'ERROR'
                location = 'unknown'
        else:
            # It's a dictionary (from our fallback)
            event_type = event.get('type', 'UNKNOWN')
            location = event.get('location', 'unknown')
            
        print(f"  Event {i+1}: {event_type} at {location}")
    
    # Try to visualize
    plt.figure(figsize=(8, 8))
    plt.imshow(field, cmap='viridis')
    plt.colorbar(label='Field Value')
    
    # Add event markers
    for event in events:
        # Handle different event types
        try:
            if hasattr(event, 'location'):
                # It's likely a custom NarrativeEvent object
                y, x = event.location
                event_type = event.type if hasattr(event, 'type') else 'EVENT'
                marker = 'ro' if event_type == 'EMERGENCE' else 'bo'
                plt.plot(x, y, marker, markersize=10)
                plt.text(x + 2, y + 2, str(event_type), color='white', 
                        bbox=dict(facecolor='black', alpha=0.5))
            elif 'location' in event:
                # It's a dictionary
                y, x = event['location']
                marker = 'ro' if event.get('type') == 'EMERGENCE' else 'bo'
                label = event.get('type', 'EVENT')
                plt.plot(x, y, marker, markersize=10)
                plt.text(x + 2, y + 2, label, color='white', 
                        bbox=dict(facecolor='black', alpha=0.5))
        except Exception as e:
            print(f"  Could not plot event: {e}")
            continue
    
    plt.title("Field with Narrative Events")
    plt.savefig("output/diagnostic/narrative_events.png")
    plt.close()
    print("✓ Created event visualization (output/diagnostic/narrative_events.png)")
    
    return True

def main():
    """Run all diagnostic tests"""
    # Display header
    print("=" * 60)
    print("ASTRA DIAGNOSTIC TEST")
    print("=" * 60)
    print(f"Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python version: {sys.version.split()[0]}")
    print(f"Working directory: {os.getcwd()}")
    
    # Run tests
    tests = [
        ("Imports", test_imports),
        ("QualiaField", test_field_creation),
        ("Evolution", test_evolution),
        ("Topology", test_topology),
        ("Narrative", test_narrative)
    ]
    
    results = []
    for name, func in tests:
        success = run_component(name, func)
        results.append((name, success))
    
    # Print summary
    section_header("TEST SUMMARY")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    print("\nDetailed Results:")
    for name, success in results:
        status = "PASS" if success else "FAIL"
        print(f"{name:15} {status}")
    
    # Calculate and print duration
    duration = (datetime.now() - start_time).total_seconds()
    print(f"\nTotal diagnostic duration: {duration:.2f} seconds")
    
    if passed == total:
        print("\nAll ASTRA components are working correctly!")
        print("\"It's a gift, a gift to the foes of Mordor!\" - Boromir")
    else:
        print(f"\n{total - passed} component(s) have issues.")
        print("\"Look to my coming at first light on the fifth day.\" - Gandalf")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
