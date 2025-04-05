"""
Topological Motifs Module for ASTRA

This module implements detection and classification of topological motifs in the qualia field.
It provides tools for:
- Detecting topological motifs (cycles, clusters, voids)
- Classifying attractor types
- Visualizing the attractor landscape

These tools help identify meaningful patterns in the qualia field that correspond to
different states of consciousness and archetypal structures.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Any, Optional, Union
import networkx as nx
from scipy.ndimage import label, find_objects, gaussian_filter, maximum_filter, minimum_filter
from scipy.spatial import Delaunay
from sklearn.cluster import DBSCAN
import warnings

from .persistence import compute_persistence_diagram, compute_betti_numbers
from .ricci import compute_joy_field


# Define archetypal motif patterns
MOTIF_PATTERNS = {
    'RECURSIVE_LOOP': {
        'description': 'Self-referential thought pattern',
        'betti': [1, 1, 0],  # One component, one loop, no voids
        'joy': 'negative',   # Negative curvature (expansive)
        'stability': 'high'  # Stable over time
    },
    'EGO_CONDENSATION': {
        'description': 'Crystallization of identity structures',
        'betti': [1, 0, 0],  # One component, no loops, no voids
        'joy': 'positive',   # Positive curvature (contractive)
        'stability': 'high'  # Stable over time
    },
    'DISSOLUTION': {
        'description': 'Boundary dissolution, ego death',
        'betti': [3, 2, 0],  # Multiple components, multiple loops
        'joy': 'negative',   # Negative curvature (expansive)
        'stability': 'low'   # Unstable, transitional
    },
    'INTEGRATION': {
        'description': 'Integration of disparate elements',
        'betti': [1, 0, 1],  # One component, no loops, one void
        'joy': 'balanced',   # Mixed curvature
        'stability': 'medium' # Moderately stable
    },
    'CATHARSIS': {
        'description': 'Emotional release pattern',
        'betti': [1, 1, 1],  # One component, one loop, one void
        'joy': 'negative',   # Negative curvature (expansive)
        'stability': 'low'   # Unstable, transitional
    }
}


def detect_critical_points(field: np.ndarray, 
                          sigma: float = 1.0) -> Dict[str, np.ndarray]:
    """
    Detect critical points (minima, maxima, saddles) in the qualia field.
    
    Critical points are key features for understanding the topology of the field.
    
    Args:
        field: 2D qualia field array
        sigma: Smoothing parameter for Gaussian filter
        
    Returns:
        Dictionary with arrays of critical point coordinates:
        - 'minima': Local minima coordinates
        - 'maxima': Local maxima coordinates
        - 'saddles': Saddle point coordinates (approximate)
    """
    try:
        # Smooth the field to reduce noise
        if sigma > 0:
            smoothed = gaussian_filter(field, sigma=sigma)
        else:
            smoothed = field
    
        # Find local maxima
        max_filtered = maximum_filter(smoothed, size=3)
        maxima = (smoothed == max_filtered) & (smoothed != smoothed.min())
        maxima_coords = np.argwhere(maxima)
        
        # Find local minima
        min_filtered = minimum_filter(smoothed, size=3)
        minima = (smoothed == min_filtered) & (smoothed != smoothed.max())
        minima_coords = np.argwhere(minima)
        
        # Approximate saddle points using Laplacian
        # True saddle detection requires more sophisticated methods
        from scipy.ndimage import laplace
        laplacian = laplace(smoothed)
        saddle_candidates = (np.abs(laplacian) < 0.01) & ~maxima & ~minima
        
        # Further filter saddle candidates by checking neighbors
        saddle_coords = []
        for y, x in np.argwhere(saddle_candidates):
            if 0 < y < field.shape[0]-1 and 0 < x < field.shape[1]-1:
                # Extract 3x3 neighborhood
                neighborhood = smoothed[y-1:y+2, x-1:x+2].copy()
                center_val = neighborhood[1, 1]
                neighborhood[1, 1] = np.nan  # Exclude center
                
                # Check if there are both higher and lower neighbors
                if (np.nanmin(neighborhood) < center_val < np.nanmax(neighborhood)):
                    # Check for saddle-like pattern
                    corners = [neighborhood[0, 0], neighborhood[0, 2], 
                              neighborhood[2, 0], neighborhood[2, 2]]
                    edges = [neighborhood[0, 1], neighborhood[1, 0], 
                            neighborhood[1, 2], neighborhood[2, 1]]
                    
                    # Simple saddle check: alternating high-low pattern
                    if ((np.mean(corners) > center_val and np.mean(edges) < center_val) or
                        (np.mean(corners) < center_val and np.mean(edges) > center_val)):
                        saddle_coords.append((y, x))
    
        saddle_coords = np.array(saddle_coords) if saddle_coords else np.zeros((0, 2), dtype=int)
        
        return {
            'minima': minima_coords,
            'maxima': maxima_coords,
            'saddles': saddle_coords
        }
    except Exception as e:
        warnings.warn(f"Error detecting critical points: {e}")
        # Return empty arrays as fallback
        return {
            'minima': np.zeros((0, 2), dtype=int),
            'maxima': np.zeros((0, 2), dtype=int),
            'saddles': np.zeros((0, 2), dtype=int)
        }


def detect_basins(field: np.ndarray, 
                 critical_points: Optional[Dict[str, np.ndarray]] = None,
                 sigma: float = 1.0) -> np.ndarray:
    """
    Detect basins of attraction in the qualia field.
    
    Basins are regions that flow to the same local minimum.
    
    Args:
        field: 2D qualia field array
        critical_points: Critical points from detect_critical_points (computed if None)
        sigma: Smoothing parameter for Gaussian filter
        
    Returns:
        Labeled array where each basin has a unique integer label
    """
    # Smooth the field to reduce noise
    if sigma > 0:
        smoothed = gaussian_filter(field, sigma=sigma)
    else:
        smoothed = field
    
    # Get critical points if not provided
    if critical_points is None:
        critical_points = detect_critical_points(smoothed, sigma=0)
    
    # Create a marker array for watershed
    markers = np.zeros_like(smoothed, dtype=int)
    
    # Mark each minimum with a unique label
    for i, (y, x) in enumerate(critical_points['minima']):
        markers[y, x] = i + 1
    
    # Use watershed to find basins
    from scipy.ndimage import watershed_ift
    
    # Create a simple neighborhood structure for watershed
    structure = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=bool)
    
    # Invert the field for watershed (watershed finds basins around minima)
    basins = watershed_ift(-smoothed, markers, structure=structure)
    
    return basins


def detect_topological_motifs(field: np.ndarray, 
                            threshold: float = 0.0,
                            sigma: float = 1.0) -> Dict[str, Any]:
    """
    Detect topological motifs in the qualia field.
    
    This combines persistence homology, critical point analysis, and basin detection
    to identify meaningful topological structures.
    
    Args:
        field: 2D qualia field array
        threshold: Value threshold for including points
        sigma: Smoothing parameter for Gaussian filter
        
    Returns:
        Dictionary with detected motifs and their properties
    """
    # Smooth the field to reduce noise
    if sigma > 0:
        smoothed = gaussian_filter(field, sigma=sigma)
    else:
        smoothed = field
    
    # Compute persistence diagram
    persistence_result = compute_persistence_diagram(smoothed, max_dim=2)
    
    # Compute Betti numbers at the threshold
    betti = compute_betti_numbers(persistence_result['diagrams'], threshold)
    
    # Detect critical points
    critical_points = detect_critical_points(smoothed, sigma=0)
    
    # Detect basins
    basins = detect_basins(smoothed, critical_points, sigma=0)
    
    # Compute joy field (negative Ricci curvature)
    joy_field = compute_joy_field(smoothed, threshold=threshold)
    
    # Determine overall joy character
    joy_mean = np.mean(joy_field)
    joy_std = np.std(joy_field)
    
    if joy_mean > joy_std:
        joy_character = 'positive'
    elif joy_mean < -joy_std:
        joy_character = 'negative'
    else:
        joy_character = 'balanced'
    
    # Identify motifs based on topological features
    motifs = []
    
    for name, pattern in MOTIF_PATTERNS.items():
        # Check if Betti numbers match the pattern
        betti_match = True
        for i, (b_actual, b_pattern) in enumerate(zip(betti, pattern['betti'])):
            # Allow for some flexibility in matching
            if i == 0:  # β₀ (connected components)
                if b_actual != b_pattern and not (b_pattern == 1 and b_actual > 0):
                    betti_match = False
                    break
            else:  # Higher Betti numbers
                if b_actual != b_pattern and not (b_pattern > 0 and b_actual > 0):
                    betti_match = False
                    break
        
        # Check if joy character matches
        joy_match = (pattern['joy'] == joy_character)
        
        # If both match, add this motif
        if betti_match and joy_match:
            motifs.append({
                'name': name,
                'description': pattern['description'],
                'confidence': 0.7 if betti_match and joy_match else 0.4,
                'stability': pattern['stability']
            })
    
    # If no motifs match exactly, find the closest one
    if not motifs:
        best_match = None
        best_score = -1
        
        for name, pattern in MOTIF_PATTERNS.items():
            # Score based on Betti number similarity and joy character
            score = 0
            for i, (b_actual, b_pattern) in enumerate(zip(betti, pattern['betti'])):
                if b_actual == b_pattern:
                    score += 1
                elif (b_pattern > 0 and b_actual > 0) or (b_pattern == 0 and b_actual == 0):
                    score += 0.5
            
            if pattern['joy'] == joy_character:
                score += 1
            
            if score > best_score:
                best_score = score
                best_match = name
        
        if best_match:
            motifs.append({
                'name': best_match,
                'description': MOTIF_PATTERNS[best_match]['description'],
                'confidence': 0.3,  # Low confidence for approximate match
                'stability': MOTIF_PATTERNS[best_match]['stability']
            })
    
    return {
        'betti_numbers': betti,
        'critical_points': critical_points,
        'basins': basins,
        'joy_character': joy_character,
        'motifs': motifs,
        'persistence_result': persistence_result
    }


def classify_attractor_type(field: np.ndarray, 
                          sigma: float = 1.0) -> Dict[str, Any]:
    """
    Classify the type of attractor present in the qualia field.
    
    This analyzes the field to determine if it contains:
    - Fixed point attractors
    - Limit cycles
    - Strange attractors
    - Multiple basins
    
    Args:
        field: 2D qualia field array
        sigma: Smoothing parameter for Gaussian filter
        
    Returns:
        Dictionary with attractor classification and properties
    """
    # Smooth the field to reduce noise
    if sigma > 0:
        smoothed = gaussian_filter(field, sigma=sigma)
    else:
        smoothed = field
    
    # Detect critical points
    critical_points = detect_critical_points(smoothed, sigma=0)
    
    # Count different types of critical points
    n_minima = len(critical_points['minima'])
    n_maxima = len(critical_points['maxima'])
    n_saddles = len(critical_points['saddles'])
    
    # Detect basins
    basins = detect_basins(smoothed, critical_points, sigma=0)
    
    # Count unique basins (excluding background)
    unique_basins = np.unique(basins)
    unique_basins = unique_basins[unique_basins > 0]
    n_basins = len(unique_basins)
    
    # Compute persistence diagram
    persistence_result = compute_persistence_diagram(smoothed, max_dim=2)
    
    # Get Betti numbers
    betti = compute_betti_numbers(persistence_result['diagrams'])
    
    # Classify attractor type
    attractor_type = 'unknown'
    confidence = 0.5
    description = ''
    
    if n_minima == 1 and n_basins == 1 and betti[1] == 0:
        # Single minimum, single basin, no loops
        attractor_type = 'fixed_point'
        confidence = 0.9
        description = 'Single fixed point attractor (stable equilibrium)'
    
    elif n_minima > 1 and n_basins > 1:
        # Multiple minima and basins
        attractor_type = 'multiple_fixed_points'
        confidence = 0.8
        description = f'Multiple fixed point attractors ({n_basins} basins)'
    
    elif betti[1] == 1 and n_minima == 0:
        # One loop, no minima
        attractor_type = 'limit_cycle'
        confidence = 0.7
        description = 'Limit cycle attractor (periodic behavior)'
    
    elif betti[1] > 1:
        # Multiple loops
        attractor_type = 'complex_periodic'
        confidence = 0.6
        description = f'Complex periodic attractor ({betti[1]} cycles)'
    
    elif betti[1] > 0 and betti[2] > 0:
        # Loops and voids - complex topology
        attractor_type = 'strange_attractor'
        confidence = 0.7
        description = 'Strange attractor (chaotic behavior)'
    
    return {
        'attractor_type': attractor_type,
        'confidence': confidence,
        'description': description,
        'n_minima': n_minima,
        'n_maxima': n_maxima,
        'n_saddles': n_saddles,
        'n_basins': n_basins,
        'betti_numbers': betti,
        'critical_points': critical_points,
        'basins': basins
    }


def plot_attractor_landscape(field: np.ndarray,
                           classification: Optional[Dict[str, Any]] = None,
                           sigma: float = 1.0,
                           ax: Optional[plt.Axes] = None) -> plt.Axes:
    """
    Plot the attractor landscape of the qualia field.
    
    This visualizes the critical points, basins, and flow of the field.
    
    Args:
        field: 2D qualia field array
        classification: Result from classify_attractor_type (computed if None)
        sigma: Smoothing parameter for Gaussian filter
        ax: Matplotlib axes to plot on (creates new if None)
        
    Returns:
        Matplotlib axes with the plot
    """
    # Smooth the field to reduce noise
    if sigma > 0:
        smoothed = gaussian_filter(field, sigma=sigma)
    else:
        smoothed = field
    
    # Get classification if not provided
    if classification is None:
        classification = classify_attractor_type(smoothed, sigma=0)
    
    # Create plot
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 8))
    
    # Plot the field as a contour
    contour = ax.contourf(smoothed, cmap='viridis', alpha=0.7, levels=20)
    plt.colorbar(contour, ax=ax, label='Field Value')
    
    # Plot critical points
    critical_points = classification['critical_points']
    
    if len(critical_points['minima']) > 0:
        ax.scatter(critical_points['minima'][:, 1], critical_points['minima'][:, 0], 
                 color='blue', marker='o', s=50, label='Minima')
    
    if len(critical_points['maxima']) > 0:
        ax.scatter(critical_points['maxima'][:, 1], critical_points['maxima'][:, 0], 
                 color='red', marker='^', s=50, label='Maxima')
    
    if len(critical_points['saddles']) > 0:
        ax.scatter(critical_points['saddles'][:, 1], critical_points['saddles'][:, 0], 
                 color='green', marker='s', s=50, label='Saddles')
    
    # Plot basin boundaries
    from skimage.segmentation import find_boundaries
    basins = classification['basins']
    if basins is not None and np.max(basins) > 0:
        boundaries = find_boundaries(basins, mode='outer')
        ax.contour(boundaries, colors='white', linewidths=0.5, levels=[0.5])
    
    # Plot flow field using quiver
    y, x = np.mgrid[0:field.shape[0]:5, 0:field.shape[1]:5]
    dy, dx = np.gradient(-smoothed)  # Negative gradient for flow direction
    
    # Normalize the vectors
    magnitude = np.sqrt(dx**2 + dy**2)
    mask = magnitude > 0
    dx_norm = np.zeros_like(dx)
    dy_norm = np.zeros_like(dy)
    dx_norm[mask] = dx[mask] / magnitude[mask]
    dy_norm[mask] = dy[mask] / magnitude[mask]
    
    # Plot flow vectors
    ax.quiver(x, y, dx_norm[::5, ::5], dy_norm[::5, ::5], 
             color='white', alpha=0.5, scale=30)
    
    # Add title and legend
    title = f"Attractor Landscape: {classification['attractor_type'].replace('_', ' ').title()}"
    if classification['description']:
        title += f"\n{classification['description']}"
    
    ax.set_title(title)
    ax.legend(loc='upper right')
    
    # Set axis labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    
    return ax
