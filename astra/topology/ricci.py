"""
Ricci Curvature Module for ASTRA

This module implements Ricci curvature computation for the qualia field.
It provides tools for:
- Computing Ollivier-Ricci curvature
- Computing Forman-Ricci curvature
- Visualizing Ricci curvature

These tools help identify regions of positive and negative curvature in the qualia field,
which correspond to different states of consciousness (e.g., joy as negative curvature).
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Any, Optional, Union
from scipy.spatial.distance import pdist, squareform
from scipy.ndimage import gaussian_filter
import warnings

# Safely import NetworkX
try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False
    warnings.warn("NetworkX not found. Using simplified Ricci computation. For full capabilities, install: pip install networkx")

# Safely import GraphRicciCurvature
try:
    from graphriccicurvature.OllivierRicci import OllivierRicci
    from graphriccicurvature.FormanRicci import FormanRicci
    GRAPHRICCI_AVAILABLE = True
except ImportError:
    GRAPHRICCI_AVAILABLE = False
    warnings.warn("GraphRicciCurvature not found. Using simplified Ricci computation. For full capabilities, install: pip install graphriccicurvature")


def field_to_graph(field: np.ndarray, threshold: float = 0.0, 
                   connectivity: int = 8, sigma: float = 1.0) -> Any:
    """
    Convert a qualia field to a weighted graph for Ricci curvature computation.
    
    Args:
        field: 2D qualia field array
        threshold: Value threshold for including nodes
        connectivity: 4 or 8 for grid connectivity
        sigma: Smoothing parameter for Gaussian filter
        
    Returns:
        NetworkX graph with nodes at field points and weighted edges or None if NetworkX is not available
    """
    # Check if NetworkX is available
    if not NETWORKX_AVAILABLE:
        warnings.warn("NetworkX is required for graph creation, using simplified approach.")
        return None
        
    try:
        # Optional smoothing
        if sigma > 0:
            smoothed_field = gaussian_filter(field, sigma=sigma)
        else:
            smoothed_field = field
        
        # Create graph
        G = nx.Graph()
        
        # Add nodes for points above threshold
        height, width = field.shape
        for y in range(height):
            for x in range(width):
                if smoothed_field[y, x] > threshold:
                    # Node position is (x, y), value is field value
                    G.add_node((x, y), value=smoothed_field[y, x], pos=(x, y))
        
        # Add edges based on connectivity
        for y in range(height):
            for x in range(width):
                if (x, y) not in G:
                    continue
                    
                # 4-connectivity: up, down, left, right
                neighbors = [
                    (x+1, y), (x-1, y), (x, y+1), (x, y-1)
                ]
                
                # Add diagonal neighbors for 8-connectivity
                if connectivity == 8:
                    neighbors.extend([
                        (x+1, y+1), (x-1, y-1), (x+1, y-1), (x-1, y+1)
                    ])
                
                # Add edges to valid neighbors
                for nbr_x, nbr_y in neighbors:
                    if 0 <= nbr_x < width and 0 <= nbr_y < height and (nbr_x, nbr_y) in G:
                        # Edge weight is average of node values
                        weight = (G.nodes[(x, y)]['value'] + G.nodes[(nbr_x, nbr_y)]['value']) / 2
                        G.add_edge((x, y), (nbr_x, nbr_y), weight=weight)
        
        return G
    except Exception as e:
        warnings.warn(f"Error creating graph from field: {e}")
        # Return empty graph as fallback
        return nx.Graph() if NETWORKX_AVAILABLE else None


def compute_ollivier_ricci_curvature(field: np.ndarray, 
                                   threshold: float = 0.0,
                                   alpha: float = 0.5,
                                   connectivity: int = 8,
                                   sigma: float = 1.0) -> Tuple[Any, np.ndarray]:
    """
    Compute Ollivier-Ricci curvature for a qualia field.
    
    Ollivier-Ricci curvature measures how much geodesics spread or converge,
    capturing the intuitive notion of curvature in discrete spaces.
    
    Args:
        field: 2D qualia field array
        threshold: Value threshold for including nodes
        alpha: Parameter controlling the influence of the graph structure
        connectivity: 4 or 8 for grid connectivity
        sigma: Smoothing parameter for Gaussian filter
        
    Returns:
        Tuple of (graph with curvature attributes, curvature field array)
    """
    # Convert field to graph
    G = field_to_graph(field, threshold, connectivity, sigma)
    
    if len(G) == 0:
        # Empty graph, return empty results
        return G, np.zeros_like(field)
    
    # Compute Ollivier-Ricci curvature
    if GRAPHRICCI_AVAILABLE:
        # Use GraphRicciCurvature package for accurate computation
        orc = OllivierRicci(G, alpha=alpha, verbose="ERROR")
        G = orc.compute_ricci_curvature()
    else:
        # Simplified approximation based on local structure
        _compute_simplified_ollivier_ricci(G)
    
    # Convert graph curvature to field array
    curvature_field = np.zeros_like(field)
    
    try:
        # Fill in curvature values from edges
        for edge in G.edges():
            (x1, y1), (x2, y2) = edge
            curvature = G[edge[0]][edge[1]].get('ricciCurvature', 0)
            
            # Set curvature at both endpoints
            deg1 = max(1, G.degree(edge[0]))  # Avoid division by zero
            deg2 = max(1, G.degree(edge[1]))  # Avoid division by zero
            curvature_field[y1, x1] += curvature / deg1
            curvature_field[y2, x2] += curvature / deg2
        
        # Normalize by node degree
        for node in G.nodes():
            x, y = node
            deg = max(1, G.degree(node))  # Avoid division by zero
            curvature_field[y, x] /= deg
    except Exception as e:
        warnings.warn(f"Error processing curvature field: {e}")
        # Fallback to a simple curvature approximation
        from scipy.ndimage import gaussian_filter, laplace
        smooth_field = gaussian_filter(field, sigma=sigma)
        curvature_field = -laplace(smooth_field)
    
    return G, curvature_field


def _compute_simplified_ollivier_ricci(G: nx.Graph) -> None:
    """
    Compute a simplified approximation of Ollivier-Ricci curvature.
    
    This is used when the GraphRicciCurvature package is not available.
    It's a rough approximation based on local structure.
    
    Args:
        G: NetworkX graph to compute curvature for
        
    Returns:
        None (modifies graph in place)
    """
    # For each edge, compute a simplified curvature
    for edge in G.edges():
        u, v = edge
        
        # Get common neighbors
        u_neighbors = set(G.neighbors(u))
        v_neighbors = set(G.neighbors(v))
        common_neighbors = u_neighbors.intersection(v_neighbors)
        
        # Simplified curvature based on common neighbors
        # More common neighbors -> more positive curvature
        # Fewer common neighbors -> more negative curvature
        common_ratio = len(common_neighbors) / max(1, min(len(u_neighbors), len(v_neighbors)))
        
        # Scale to typical Ollivier-Ricci range
        curvature = 2 * common_ratio - 1
        
        # Store on edge
        G[u][v]['ricciCurvature'] = curvature


def compute_forman_ricci_curvature(field: np.ndarray,
                                 threshold: float = 0.0,
                                 connectivity: int = 8,
                                 sigma: float = 1.0) -> Tuple[nx.Graph, np.ndarray]:
    """
    Compute Forman-Ricci curvature for a qualia field.
    
    Forman-Ricci curvature is a combinatorial version of Ricci curvature
    that is simpler to compute than Ollivier-Ricci curvature.
    
    Args:
        field: 2D qualia field array
        threshold: Value threshold for including nodes
        connectivity: 4 or 8 for grid connectivity
        sigma: Smoothing parameter for Gaussian filter
        
    Returns:
        Tuple of (graph with curvature attributes, curvature field array)
    """
    # Convert field to graph
    G = field_to_graph(field, threshold, connectivity, sigma)
    
    if len(G) == 0:
        # Empty graph, return empty results
        return G, np.zeros_like(field)
    
    # Compute Forman-Ricci curvature
    if GRAPHRICCI_AVAILABLE:
        # Use GraphRicciCurvature package for accurate computation
        frc = FormanRicci(G)
        G = frc.compute_ricci_curvature()
    else:
        # Simplified approximation
        _compute_simplified_forman_ricci(G)
    
    # Convert graph curvature to field array
    curvature_field = np.zeros_like(field)
    
    # Fill in curvature values from edges
    for edge in G.edges():
        (x1, y1), (x2, y2) = edge
        curvature = G[edge[0]][edge[1]]['formanCurvature']
        
        # Set curvature at both endpoints
        curvature_field[y1, x1] += curvature / G.degree(edge[0])
        curvature_field[y2, x2] += curvature / G.degree(edge[1])
    
    # Normalize by node degree
    for node in G.nodes():
        x, y = node
        if G.degree(node) > 0:
            curvature_field[y, x] /= G.degree(node)
    
    return G, curvature_field


def _compute_simplified_forman_ricci(G: nx.Graph) -> None:
    """
    Compute a simplified approximation of Forman-Ricci curvature.
    
    This is used when the GraphRicciCurvature package is not available.
    
    Args:
        G: NetworkX graph to compute curvature for
        
    Returns:
        None (modifies graph in place)
    """
    # For each edge, compute a simplified Forman curvature
    for edge in G.edges():
        u, v = edge
        
        # Basic Forman curvature formula: 2 - (deg(u) + deg(v))
        curvature = 2 - (G.degree(u) + G.degree(v))
        
        # Store on edge
        G[u][v]['formanCurvature'] = curvature


def compute_joy_field(field: np.ndarray, 
                     method: str = 'ollivier',
                     **kwargs) -> np.ndarray:
    """
    Compute the joy field as negative Ricci curvature.
    
    Joy is defined as K(χ) = -Ric(χ), where Ric is Ricci curvature.
    Negative curvature implies expansive cognition: integration without collapse.
    
    Args:
        field: 2D qualia field array
        method: 'ollivier' or 'forman' for curvature computation
        **kwargs: Additional parameters for curvature computation
        
    Returns:
        Joy field array (negative of Ricci curvature)
    """
    if method == 'ollivier':
        _, curvature_field = compute_ollivier_ricci_curvature(field, **kwargs)
    elif method == 'forman':
        _, curvature_field = compute_forman_ricci_curvature(field, **kwargs)
    else:
        raise ValueError(f"Unknown method: {method}")
    
    # Joy is negative curvature
    joy_field = -curvature_field
    
    return joy_field


def plot_ricci_curvature(G: nx.Graph, 
                        field: np.ndarray,
                        curvature_field: np.ndarray,
                        title: str = "Ricci Curvature",
                        cmap: str = 'coolwarm',
                        show_graph: bool = True,
                        ax: Optional[plt.Axes] = None) -> plt.Axes:
    """
    Plot Ricci curvature for a qualia field.
    
    Args:
        G: NetworkX graph with curvature attributes
        field: Original qualia field array
        curvature_field: Curvature field array
        title: Plot title
        cmap: Colormap to use
        show_graph: Whether to overlay graph edges
        ax: Matplotlib axes to plot on (creates new if None)
        
    Returns:
        Matplotlib axes with the plot
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 8))
    
    # Plot curvature field
    im = ax.imshow(curvature_field, cmap=cmap, origin='lower', interpolation='nearest')
    plt.colorbar(im, ax=ax, label='Ricci Curvature')
    
    # Overlay graph edges if requested
    if show_graph and len(G) > 0:
        # Get node positions
        pos = nx.get_node_attributes(G, 'pos')
        
        # Get edge curvatures
        edge_curvature = {}
        for u, v in G.edges():
            if 'ricciCurvature' in G[u][v]:
                edge_curvature[(u, v)] = G[u][v]['ricciCurvature']
            elif 'formanCurvature' in G[u][v]:
                edge_curvature[(u, v)] = G[u][v]['formanCurvature']
        
        # Draw edges with curvature-based colors
        if edge_curvature:
            edges = list(edge_curvature.keys())
            curvatures = list(edge_curvature.values())
            
            # Normalize curvatures for coloring
            vmin = min(curvatures)
            vmax = max(curvatures)
            
            # Draw edges with curvature-based colors
            for edge, curv in zip(edges, curvatures):
                u, v = edge
                x1, y1 = pos[u]
                x2, y2 = pos[v]
                
                # Normalize curvature to [0, 1]
                norm_curv = (curv - vmin) / (vmax - vmin) if vmax > vmin else 0.5
                
                # Get color from colormap
                color = plt.cm.coolwarm(norm_curv)
                
                # Draw edge
                ax.plot([x1, x2], [y1, y2], color=color, alpha=0.5, linewidth=1)
    
    # Set labels and title
    ax.set_title(title)
    ax.set_xticks([])
    ax.set_yticks([])
    
    return ax
