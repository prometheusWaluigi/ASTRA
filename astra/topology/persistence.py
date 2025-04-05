"""
Persistence Homology Module for ASTRA

This module implements persistent homology computation for the qualia field.
It provides tools for:
- Computing persistence diagrams
- Calculating Betti numbers
- Visualizing persistence landscapes

These tools help identify topological features (connected components, loops, voids)
across multiple scales in the qualia field.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Any, Optional, Union
from scipy.spatial.distance import pdist, squareform
from scipy.ndimage import gaussian_filter
import networkx as nx
from collections import defaultdict
import warnings

# For advanced TDA, we'll use ripser if available
try:
    import ripser
    RIPSER_AVAILABLE = True
except ImportError:
    RIPSER_AVAILABLE = False
    warnings.warn("Ripser not found. Using simplified persistence computation. For full TDA capabilities, install: pip install ripser")


def prepare_point_cloud(field: np.ndarray, threshold: float = 0.0, 
                       max_points: int = 1000, sigma: float = 1.0) -> np.ndarray:
    """
    Prepare a point cloud from a qualia field for persistence computation.
    
    This converts the 2D field into a point cloud by:
    1. Smoothing the field (optional)
    2. Thresholding to keep only significant points
    3. Extracting coordinates and values as a point cloud
    
    Args:
        field: 2D qualia field array
        threshold: Value threshold for including points
        max_points: Maximum number of points to include (for performance)
        sigma: Smoothing parameter for Gaussian filter
        
    Returns:
        Array of shape (n_points, 3) with x, y coordinates and field values
    """
    try:
        # Optional smoothing
        if sigma > 0:
            smoothed_field = gaussian_filter(field, sigma=sigma)
        else:
            smoothed_field = field
        
        # Find points above threshold
        y_indices, x_indices = np.where(smoothed_field > threshold)
        values = smoothed_field[y_indices, x_indices]
        
        # Create point cloud with coordinates and values
        point_cloud = np.column_stack((x_indices, y_indices, values))
        
        # Subsample if too many points
        if len(point_cloud) > max_points:
            indices = np.random.choice(len(point_cloud), max_points, replace=False)
            point_cloud = point_cloud[indices]
        
        return point_cloud
    except Exception as e:
        warnings.warn(f"Error preparing point cloud: {e}")
        # Return a minimal point cloud as fallback
        return np.array([[0, 0, 0], [1, 1, 1]])


def compute_persistence_diagram(data: Union[np.ndarray, List[np.ndarray]], 
                              max_dim: int = 2,
                              method: str = 'ripser',
                              **kwargs) -> Dict[str, Any]:
    """
    Compute the persistence diagram for a dataset.
    
    Args:
        data: Input data, either:
              - Point cloud (n_points, n_dimensions)
              - Distance matrix (n_points, n_points)
              - 2D field array (will be converted to point cloud)
              - List of field states for tracking evolution
        max_dim: Maximum homology dimension to compute
        method: 'ripser' (preferred) or 'custom' (simplified)
        **kwargs: Additional parameters for specific methods
        
    Returns:
        Dictionary containing:
        - 'diagrams': List of persistence diagrams for each dimension
        - 'betti_curves': Betti curves for each dimension
        - 'method': Method used for computation
        - Additional method-specific results
    """
    # Process input data
    if isinstance(data, list):
        # List of field states - compute for each and return list of results
        results = []
        for field in data:
            result = compute_persistence_diagram(field, max_dim, method, **kwargs)
            results.append(result)
        return {
            'diagrams': [r['diagrams'] for r in results],
            'betti_curves': [r['betti_curves'] for r in results],
            'method': method,
            'multi_state': True,
            'results': results
        }
    
    # Convert 2D field to point cloud if needed
    if len(data.shape) == 2:
        data = prepare_point_cloud(
            data, 
            threshold=kwargs.get('threshold', 0.0),
            max_points=kwargs.get('max_points', 1000),
            sigma=kwargs.get('sigma', 1.0)
        )
    
    # Compute persistence diagram
    if method == 'ripser' and RIPSER_AVAILABLE:
        # Use Ripser for efficient computation
        ripser_kwargs = {
            'maxdim': max_dim,
            'thresh': kwargs.get('thresh', np.inf),
            'coeff': kwargs.get('coeff', 2),  # Z/2Z coefficients
            'do_cocycles': kwargs.get('do_cocycles', False)
        }
        
        # Check if input is distance matrix
        if len(data.shape) == 2 and data.shape[0] == data.shape[1]:
            ripser_kwargs['distance_matrix'] = True
        
        # Compute using ripser
        result = ripser.ripser(data, **ripser_kwargs)
        
        # Extract diagrams
        diagrams = result['dgms']
        
        # Compute Betti curves
        betti_curves = compute_betti_curves(diagrams, resolution=100)
        
        return {
            'diagrams': diagrams,
            'betti_curves': betti_curves,
            'method': 'ripser',
            'ripser_result': result
        }
    
    else:
        # Use simplified custom implementation
        return _compute_persistence_custom(data, max_dim, **kwargs)


def _compute_persistence_custom(data: np.ndarray, max_dim: int = 2, 
                              **kwargs) -> Dict[str, Any]:
    """
    Simplified custom implementation of persistence diagram computation.
    
    This is a basic implementation for when Ripser is not available.
    It only computes accurate diagrams for dimension 0 (connected components)
    and provides approximations for higher dimensions.
    
    Args:
        data: Point cloud or distance matrix
        max_dim: Maximum homology dimension
        **kwargs: Additional parameters
        
    Returns:
        Dictionary with persistence results
    """
    # Compute distance matrix if input is point cloud
    if len(data.shape) == 2 and data.shape[0] != data.shape[1]:
        distances = squareform(pdist(data))
    else:
        distances = data
    
    # Create filtration by thresholding distance matrix
    n_points = distances.shape[0]
    resolution = kwargs.get('resolution', 100)
    max_dist = np.max(distances)
    thresholds = np.linspace(0, max_dist, resolution)
    
    # Initialize diagrams for each dimension
    diagrams = [[] for _ in range(max_dim + 1)]
    
    # Dimension 0: Connected components
    # Track when points merge into connected components
    uf = UnionFind(n_points)
    births = np.zeros(n_points)  # All components born at threshold 0
    
    # Sort edges by distance
    edges = []
    for i in range(n_points):
        for j in range(i+1, n_points):
            edges.append((i, j, distances[i, j]))
    edges.sort(key=lambda x: x[2])
    
    # Process edges in order of increasing distance
    for i, j, dist in edges:
        if uf.find(i) != uf.find(j):
            # Merge components and record death of one component
            root_i, root_j = uf.find(i), uf.find(j)
            uf.union(i, j)
            # The component that died is the one with higher root index (arbitrary)
            dying_root = max(root_i, root_j)
            diagrams[0].append((0, dist))  # Birth at 0, death at current distance
    
    # Approximate higher dimensions (simplified)
    if max_dim >= 1:
        # Create a graph from the distance matrix
        G = nx.Graph()
        for i in range(n_points):
            G.add_node(i)
        
        # Add edges based on distance thresholds
        for t_idx, threshold in enumerate(thresholds):
            # Add edges for this threshold
            for i in range(n_points):
                for j in range(i+1, n_points):
                    if distances[i, j] <= threshold and not G.has_edge(i, j):
                        G.add_edge(i, j)
            
            # Count cycles (dimension 1)
            if max_dim >= 1:
                # Number of 1-cycles is approximately: |E| - |V| + |CC|
                n_edges = G.number_of_edges()
                n_vertices = G.number_of_nodes()
                n_components = nx.number_connected_components(G)
                n_cycles = max(0, n_edges - n_vertices + n_components)
                
                # Add births/deaths based on cycle count changes
                # (This is a very rough approximation)
                if t_idx > 0 and n_cycles > len(diagrams[1]):
                    # New cycles born
                    for _ in range(n_cycles - len(diagrams[1])):
                        diagrams[1].append((threshold, np.inf))
    
    # Convert to numpy arrays
    for dim in range(len(diagrams)):
        if diagrams[dim]:
            diagrams[dim] = np.array(diagrams[dim])
        else:
            diagrams[dim] = np.zeros((0, 2))
    
    # Compute Betti curves
    betti_curves = compute_betti_curves(diagrams, resolution=resolution)
    
    return {
        'diagrams': diagrams,
        'betti_curves': betti_curves,
        'method': 'custom',
        'thresholds': thresholds
    }


def compute_betti_curves(diagrams: List[np.ndarray], 
                        resolution: int = 100) -> np.ndarray:
    """
    Compute Betti curves from persistence diagrams.
    
    Betti curves show the number of topological features (of each dimension)
    that persist at each threshold value.
    
    Args:
        diagrams: List of persistence diagrams for each dimension
        resolution: Number of points in the curves
        
    Returns:
        Array of shape (n_dimensions, resolution) with Betti curves
    """
    # Find min and max birth/death values across all diagrams
    min_val = np.inf
    max_val = -np.inf
    
    for dim, diagram in enumerate(diagrams):
        if len(diagram) > 0:
            min_val = min(min_val, np.min(diagram[np.isfinite(diagram)]))
            max_val = max(max_val, np.max(diagram[np.isfinite(diagram)]))
    
    if min_val == np.inf:
        min_val = 0
    if max_val == -np.inf:
        max_val = 1
    
    # Create threshold values
    thresholds = np.linspace(min_val, max_val, resolution)
    
    # Initialize Betti curves
    betti_curves = np.zeros((len(diagrams), resolution))
    
    # Compute Betti number at each threshold
    for dim, diagram in enumerate(diagrams):
        if len(diagram) == 0:
            continue
            
        for i, threshold in enumerate(thresholds):
            # Count features born before and dying after the threshold
            births = diagram[:, 0]
            deaths = diagram[:, 1]
            
            # Handle infinite death times
            finite_deaths = deaths.copy()
            finite_deaths[np.isinf(finite_deaths)] = max_val * 1.1
            
            # Count features alive at this threshold
            alive = np.sum((births <= threshold) & (finite_deaths > threshold))
            betti_curves[dim, i] = alive
    
    return betti_curves


def compute_betti_numbers(diagrams: List[np.ndarray], 
                         threshold: Optional[float] = None) -> List[int]:
    """
    Compute Betti numbers at a specific threshold from persistence diagrams.
    
    Betti numbers count the number of topological features in each dimension:
    - β₀: number of connected components
    - β₁: number of 1-dimensional holes (loops)
    - β₂: number of 2-dimensional voids
    
    Args:
        diagrams: List of persistence diagrams for each dimension
        threshold: Specific threshold to compute Betti numbers at
                  (if None, use the median of all finite values)
        
    Returns:
        List of Betti numbers for each dimension
    """
    # Determine threshold if not provided
    if threshold is None:
        all_values = []
        for diagram in diagrams:
            if len(diagram) > 0:
                all_values.extend(diagram[np.isfinite(diagram)].flatten())
        
        if all_values:
            threshold = np.median(all_values)
        else:
            threshold = 0.0
    
    # Compute Betti numbers
    betti_numbers = []
    
    for dim, diagram in enumerate(diagrams):
        if len(diagram) == 0:
            betti_numbers.append(0)
            continue
            
        # Count features born before and dying after the threshold
        births = diagram[:, 0]
        deaths = diagram[:, 1]
        
        # Handle infinite death times
        finite_deaths = deaths.copy()
        finite_deaths[np.isinf(finite_deaths)] = threshold * 1.1
        
        # Count features alive at this threshold
        alive = np.sum((births <= threshold) & (finite_deaths > threshold))
        betti_numbers.append(int(alive))
    
    return betti_numbers


def persistence_landscape(diagrams: List[np.ndarray], 
                         dim: int = 1,
                         resolution: int = 100) -> np.ndarray:
    """
    Compute the persistence landscape for a specific homology dimension.
    
    Persistence landscapes are functional summaries of persistence diagrams
    that have nice mathematical properties for statistical analysis.
    
    Args:
        diagrams: List of persistence diagrams for each dimension
        dim: Homology dimension to compute landscape for
        resolution: Number of points in the landscape
        
    Returns:
        Array of shape (n_landscapes, resolution) with landscape functions
    """
    if dim >= len(diagrams) or len(diagrams[dim]) == 0:
        return np.zeros((1, resolution))
    
    diagram = diagrams[dim]
    
    # Find min and max birth/death values
    min_val = np.min(diagram[np.isfinite(diagram)])
    max_val = np.max(diagram[np.isfinite(diagram)])
    
    # Handle infinite death times
    finite_diagram = diagram.copy()
    finite_diagram[np.isinf(finite_diagram)] = max_val * 1.1
    
    # Create grid for landscape
    grid = np.linspace(min_val, max_val * 1.1, resolution)
    
    # Compute landscape functions
    n_points = len(diagram)
    landscape_values = []
    
    for i in range(n_points):
        birth, death = finite_diagram[i]
        midpoint = (birth + death) / 2
        
        # Create piecewise linear function for this point
        values = np.zeros(resolution)
        for j, x in enumerate(grid):
            if birth <= x <= midpoint:
                values[j] = x - birth
            elif midpoint <= x <= death:
                values[j] = death - x
            else:
                values[j] = 0
        
        landscape_values.append(values)
    
    # Sort landscape functions by height
    if landscape_values:
        landscape_values = np.array(landscape_values)
        max_heights = np.max(landscape_values, axis=1)
        sorted_indices = np.argsort(max_heights)[::-1]
        landscape_values = landscape_values[sorted_indices]
    else:
        landscape_values = np.zeros((1, resolution))
    
    return landscape_values


def plot_persistence_diagram(diagrams: List[np.ndarray], 
                           title: str = "Persistence Diagram",
                           max_dim: int = 2,
                           ax: Optional[plt.Axes] = None) -> plt.Axes:
    """
    Plot a persistence diagram.
    
    Args:
        diagrams: List of persistence diagrams for each dimension
        title: Plot title
        max_dim: Maximum dimension to plot
        ax: Matplotlib axes to plot on (creates new if None)
        
    Returns:
        Matplotlib axes with the plot
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 8))
    
    # Colors for different dimensions
    colors = ['blue', 'red', 'green', 'purple', 'orange']
    markers = ['o', 's', '^', 'D', 'v']
    
    # Plot diagrams for each dimension
    for dim, diagram in enumerate(diagrams):
        if dim > max_dim or len(diagram) == 0:
            continue
        
        # Get finite points
        finite_mask = np.isfinite(diagram[:, 1])
        finite_diag = diagram[finite_mask]
        
        # Plot finite points
        if len(finite_diag) > 0:
            ax.scatter(
                finite_diag[:, 0], finite_diag[:, 1],
                color=colors[dim % len(colors)],
                marker=markers[dim % len(markers)],
                alpha=0.7,
                label=f"H{dim}"
            )
        
        # Plot points with infinite death separately
        inf_mask = ~finite_mask
        inf_diag = diagram[inf_mask]
        
        if len(inf_diag) > 0:
            # Find max birth value to determine where to place inf points
            if len(finite_diag) > 0:
                max_val = max(np.max(finite_diag), np.max(inf_diag[:, 0])) * 1.1
            else:
                max_val = np.max(inf_diag[:, 0]) * 1.1
            
            # Plot points with inf death at max_val
            ax.scatter(
                inf_diag[:, 0], np.ones_like(inf_diag[:, 0]) * max_val,
                color=colors[dim % len(colors)],
                marker=markers[dim % len(markers)],
                edgecolors='k',
                alpha=0.7
            )
    
    # Plot diagonal
    lims = ax.get_xlim() + ax.get_ylim()
    min_val = min(lims)
    max_val = max(lims)
    ax.plot([min_val, max_val], [min_val, max_val], 'k--', alpha=0.3)
    
    # Set labels and title
    ax.set_xlabel("Birth")
    ax.set_ylabel("Death")
    ax.set_title(title)
    ax.legend()
    
    return ax


class UnionFind:
    """
    Union-Find data structure for tracking connected components.
    Used in the simplified persistence computation.
    """
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return
        
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        else:
            self.parent[root_y] = root_x
            if self.rank[root_x] == self.rank[root_y]:
                self.rank[root_x] += 1
