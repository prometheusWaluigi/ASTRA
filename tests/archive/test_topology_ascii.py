"""
ASCII-safe version of topology test for ASTRA

Tests the simplified topology analysis without Unicode characters
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt

# Make sure we can import from the astra package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import ASTRA modules
try:
    from astra.core import QualiaField, evolve
    print("[PASS] Successfully imported ASTRA core modules")
except ImportError as e:
    print(f"[ERROR] Failed to import ASTRA core modules: {e}")
    sys.exit(1)

# Create output directory if it doesn't exist
os.makedirs("output", exist_ok=True)
os.makedirs("output/topology", exist_ok=True)

print("Testing ASTRA topology module with fixed implementation...")

# Try to import the NetworkX module for graph operations
nx_available = False
try:
    import networkx as nx
    nx_available = True
    print("[PASS] NetworkX is available for topology analysis")
except ImportError:
    print("[WARNING] NetworkX is not available. Limited topology analysis will be performed.")

# Try to import our custom Ricci curvature with safe fallbacks
try:
    from astra.topology import (
        field_to_graph,
        compute_ricci_curvature,
        compute_ollivier_ricci_curvature,
        compute_forman_ricci_curvature
    )
    ricci_available = True
    print("[PASS] Ricci curvature module is available")
except ImportError as e:
    ricci_available = False
    print(f"[WARNING] Ricci curvature module is not available: {e}. Limited topology analysis will be performed.")

# Create a QualiaField
print("Creating QualiaField for topology analysis...")
field = QualiaField(grid_size=64)
print(f"[PASS] Created QualiaField with shape {field.grid.shape}")

# Evolve the field to create more interesting patterns
print("Evolving field to create interesting patterns...")
evolution_result = evolve(
    field.grid.copy(),
    duration=0.5,
    dt=0.01,
    alpha=0.5,
    beta=0.8,
    gamma=0.3,
    store_frames=5
)
evolved_field = evolution_result["final_state"]
print("[PASS] Field evolved successfully")

# Save the evolved field
plt.figure(figsize=(10, 8))
plt.imshow(evolved_field, cmap='viridis')
plt.colorbar(label='Field Value')
plt.title('Evolved Field for Topology Analysis')
plt.savefig("output/topology/evolved_field.png")
plt.close()
print("[PASS] Evolved field saved to output/topology/evolved_field.png")

# Simple thresholding to create a binary field
threshold = np.percentile(evolved_field, 75)  # Use top 25% values
binary_field = (evolved_field > threshold).astype(int)

# Save binary field
plt.figure(figsize=(10, 8))
plt.imshow(binary_field, cmap='binary')
plt.title('Binary Field (Thresholded)')
plt.savefig("output/topology/binary_field.png")
plt.close()
print("[PASS] Binary field saved to output/topology/binary_field.png")

# Create a graph from the field if NetworkX is available
if nx_available and ricci_available:
    # Convert field to graph
    print("Converting field to graph...")
    graph = field_to_graph(evolved_field, threshold=0.0, connectivity=8)
    print(f"[PASS] Created graph with {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges")
    
    # Compute basic graph metrics
    print("Computing graph metrics...")
    clustering = nx.average_clustering(graph)
    print(f"[INFO] Average clustering coefficient: {clustering:.4f}")
    
    # Try to compute components
    components = list(nx.connected_components(graph))
    print(f"[INFO] Number of connected components: {len(components)}")
    
    # Visualize the graph
    plt.figure(figsize=(10, 8))
    pos = {(i, j): (j, -i) for i, j in graph.nodes()}  # Position nodes using grid coordinates
    nx.draw(graph, pos=pos, node_size=10, node_color='blue', edge_color='gray', alpha=0.6)
    plt.title('Graph Representation of Field')
    plt.savefig("output/topology/field_graph.png")
    plt.close()
    print("[PASS] Graph visualization saved to output/topology/field_graph.png")
    
    # Try to compute Ricci curvature
    try:
        print("Computing Ricci curvature...")
        graph, curvature = compute_ricci_curvature(evolved_field, threshold=0.0)
        
        # Prepare curvature visualization
        curvature_array = np.zeros_like(evolved_field)
        for node, data in graph.nodes(data=True):
            if 'ricciCurvature' in data:
                i, j = node
                curvature_array[i, j] = data['ricciCurvature']
        
        # Visualize curvature
        plt.figure(figsize=(10, 8))
        plt.imshow(curvature_array, cmap='coolwarm')
        plt.colorbar(label='Ricci Curvature')
        plt.title('Ricci Curvature of Field')
        plt.savefig("output/topology/ricci_curvature.png")
        plt.close()
        print("[PASS] Ricci curvature visualization saved to output/topology/ricci_curvature.png")
    except Exception as e:
        print(f"[WARNING] Could not compute Ricci curvature: {str(e)}")
else:
    print("[INFO] Skipping graph and curvature analysis due to missing dependencies")

# Simple connected component analysis using scikit-image if available
try:
    from skimage import measure
    print("Performing connected component analysis...")
    
    labeled_field, num_features = measure.label(binary_field, return_num=True, connectivity=2)
    print(f"[INFO] Number of connected components: {num_features}")
    
    # Visualize labeled components
    plt.figure(figsize=(10, 8))
    plt.imshow(labeled_field, cmap='nipy_spectral')
    plt.colorbar(label='Component ID')
    plt.title('Connected Components')
    plt.savefig("output/topology/connected_components.png")
    plt.close()
    print("[PASS] Connected components visualization saved to output/topology/connected_components.png")
    
    # Get region properties
    regions = measure.regionprops(labeled_field)
    areas = [r.area for r in regions]
    
    # Plot area distribution
    plt.figure(figsize=(10, 6))
    plt.hist(areas, bins=20)
    plt.xlabel('Component Area')
    plt.ylabel('Frequency')
    plt.title('Component Size Distribution')
    plt.savefig("output/topology/component_size_distribution.png")
    plt.close()
    print("[PASS] Component size distribution saved to output/topology/component_size_distribution.png")
except ImportError:
    print("[WARNING] scikit-image not available for connected component analysis")

print("Topology tests completed!")
