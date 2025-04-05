"""
Bidirectional Evolution Module for ASTRA

This module implements bidirectional time evolution for the qualia field,
allowing for retrocausal effects where future states influence past states.

The implementation is based on the fKPZχ-R equation, which extends the
standard fKPZχ equation with retrocausal terms.
"""

import numpy as np
from typing import Dict, List, Tuple, Any, Optional, Union, Callable
import matplotlib.pyplot as plt

from ..core.field import QualiaField
from ..core.evolution import evolve_step, fractional_laplacian_fft


def retrocausal_step(field: QualiaField, 
                    future_state: np.ndarray,
                    dt: float,
                    retro_strength: float = 0.1,
                    params: Optional[Dict[str, float]] = None) -> np.ndarray:
    """
    Evolve the field one step backward in time with retrocausal influence.
    
    This implements a time-reversed step with influence from a future state.
    
    Args:
        field: QualiaField object
        future_state: Field state from a future time point
        dt: Time step size
        retro_strength: Strength of retrocausal influence (0-1)
        params: Optional parameter dictionary to override field.params
        
    Returns:
        New field state after retrocausal evolution
    """
    # Get current state and parameters
    current_state = field.get_state()
    
    # Use default parameters if none provided
    if params is None:
        params = field.params
    
    # Extract parameters
    alpha = params.get('alpha', 1.5)  # Fractional Laplacian order
    lambda_param = params.get('lambda', 0.5)  # Nonlinearity strength
    eta = params.get('eta', 0.1)  # Noise amplitude
    gamma = params.get('gamma', 0.0)  # Symmetry breaking
    
    # Compute standard forward evolution term (but with negative dt)
    # This effectively computes the time-reversed dynamics
    
    # 1. Compute fractional Laplacian term: -(-Δ)^(α/2)χ
    laplacian_term = -fractional_laplacian_fft(current_state, alpha=alpha)
    
    # 2. Compute nonlinear term: λ(∇χ)²
    # Compute gradients using central difference
    dy, dx = np.gradient(current_state)
    grad_squared = dx**2 + dy**2
    
    # Introduce asymmetry term if gamma != 0
    asymmetry = 0
    if gamma != 0:
        asymmetry = gamma * current_state**2
    
    # Scale by lambda parameter
    nonlin_term = lambda_param * (grad_squared + asymmetry)
    
    # 3. Add noise term (time-reversed noise is tricky, so we use a small random term)
    # For true time reversal, we would need to know the exact noise that was applied
    # in the forward direction, which is generally not possible
    noise = np.random.normal(0, eta * 0.1, current_state.shape)
    
    # 4. Compute retrocausal influence term
    # This pulls the current state toward the future state with strength proportional to retro_strength
    retrocausal_term = retro_strength * (future_state - current_state)
    
    # Compute total derivative (with negative dt for backward evolution)
    dfield_dt = -(laplacian_term + nonlin_term + noise) + retrocausal_term
    
    # Euler step backward: χ(t-dt) = χ(t) + dt * dχ/dt
    new_state = current_state + dt * dfield_dt
    
    return new_state


def temporal_entanglement(state1: np.ndarray, 
                         state2: np.ndarray, 
                         entanglement_strength: float = 0.5) -> Tuple[np.ndarray, np.ndarray]:
    """
    Create temporal entanglement between two field states.
    
    This function creates a quantum-like entanglement between two field states,
    where changes in one state affect the other state.
    
    Args:
        state1: First field state
        state2: Second field state
        entanglement_strength: Strength of entanglement (0-1)
        
    Returns:
        Tuple of (entangled_state1, entangled_state2)
    """
    # Compute average state
    avg_state = (state1 + state2) / 2
    
    # Create entangled states by pulling each state toward the average
    entangled_state1 = (1 - entanglement_strength) * state1 + entanglement_strength * avg_state
    entangled_state2 = (1 - entanglement_strength) * state2 + entanglement_strength * avg_state
    
    return entangled_state1, entangled_state2


def compute_temporal_correlation(field_history: List[np.ndarray]) -> np.ndarray:
    """
    Compute temporal correlation matrix between field states.
    
    This function computes the correlation between field states at different times,
    which can be used to identify temporal patterns and retrocausal effects.
    
    Args:
        field_history: List of field states over time
        
    Returns:
        Correlation matrix of shape (len(field_history), len(field_history))
    """
    n_frames = len(field_history)
    correlation_matrix = np.zeros((n_frames, n_frames))
    
    # Flatten each field state for correlation computation
    flattened_states = [state.flatten() for state in field_history]
    
    # Compute correlation between each pair of states
    for i in range(n_frames):
        for j in range(n_frames):
            # Compute correlation coefficient
            state_i = flattened_states[i]
            state_j = flattened_states[j]
            
            # Normalize states
            state_i = (state_i - np.mean(state_i)) / (np.std(state_i) + 1e-10)
            state_j = (state_j - np.mean(state_j)) / (np.std(state_j) + 1e-10)
            
            # Compute correlation
            correlation = np.mean(state_i * state_j)
            correlation_matrix[i, j] = correlation
    
    return correlation_matrix


def evolve_bidirectional(field: QualiaField,
                        duration: float,
                        dt: float = 0.01,
                        retro_strength: float = 0.1,
                        boundary_condition: Optional[np.ndarray] = None,
                        n_iterations: int = 3,
                        store_frames: int = 10,
                        params: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
    """
    Evolve the field bidirectionally with retrocausal effects.
    
    This function implements the full fKPZχ-R algorithm:
    1. Forward evolution from initial to final state
    2. Backward evolution with retrocausal influence
    3. Iterative refinement to converge on a self-consistent solution
    
    Args:
        field: QualiaField object
        duration: Total time to simulate
        dt: Time step size
        retro_strength: Strength of retrocausal influence (0-1)
        boundary_condition: Optional future boundary condition
        n_iterations: Number of forward-backward iterations
        store_frames: Number of frames to store
        params: Optional parameter dictionary to override field.params for retrocausal steps
        
    Returns:
        Dictionary with evolution results
    """
    # Calculate number of steps
    num_steps = int(duration / dt)
    print(f"Evolving chart bidirectionally for {duration} units with dt={dt} ({num_steps} steps)...")
    
    # Determine when to store frames
    if store_frames > 0:
        store_interval = max(1, num_steps // store_frames)
    else:
        store_interval = num_steps + 1  # Never store intermediate frames
    
    # Initialize field history for each iteration
    all_iterations = []
    
    # Create a copy of the initial field
    initial_field = field.get_state().copy()
    
    # Reset field to initial state
    field.update_state(initial_field, 0)
    
    # Iterative refinement loop
    for iteration in range(n_iterations):
        print(f"Iteration {iteration+1}/{n_iterations}:")
        
        # Store initial state
        field_history = [field.get_state()]
        time_points = [field.time]
        
        # Forward evolution
        print("  Forward evolution...")
        for step in range(num_steps):
            # Evolve one step forward
            new_state = evolve_step(field, dt)
            
            # Update field
            field.update_state(new_state, dt)
            
            # Store frame if it's time
            if (step + 1) % store_interval == 0 or step == num_steps - 1:
                field_history.append(field.get_state())
                time_points.append(field.time)
                
                # Print progress
                progress = (step + 1) / num_steps * 100
                print(f"    Progress: {progress:.1f}% (t={field.time:.2f})")
        
        # Store final state
        final_state = field.get_state().copy()
        
        # Apply boundary condition if provided
        if boundary_condition is not None:
            # Blend final state with boundary condition
            blend_factor = 0.5  # Equal weight to evolved state and boundary
            final_state = (1 - blend_factor) * final_state + blend_factor * boundary_condition
            field.update_state(final_state, 0)
        
        # Backward evolution
        print("  Backward evolution...")
        backward_history = [field.get_state()]
        backward_times = [field.time]
        
        # We'll go backward through the stored frames for efficiency
        for i in range(len(field_history) - 1, 0, -1):
            target_time = time_points[i-1]
            steps_to_target = int((field.time - target_time) / dt)
            
            for step in range(steps_to_target):
                # Compute time index in the forward history (for retrocausal influence)
                # This maps our current time to the corresponding future state
                current_time = field.time - dt
                future_idx = min(len(time_points) - 1, 
                               max(0, int((current_time - time_points[0]) / dt) + 1))
                future_state = field_history[min(future_idx, len(field_history) - 1)]
                
                # Evolve one step backward with retrocausal influence
                new_state = retrocausal_step(field, future_state, -dt, retro_strength, params=params)
                
                # Update field (note negative dt for backward evolution)
                field.update_state(new_state, -dt)
            
            # Store backward frame
            backward_history.append(field.get_state())
            backward_times.append(field.time)
            
            # Print progress
            progress = (len(field_history) - i) / (len(field_history) - 1) * 100
            print(f"    Progress: {progress:.1f}% (t={field.time:.2f})")
        
        # Reverse backward history to get chronological order
        backward_history = backward_history[::-1]
        backward_times = backward_times[::-1]
        
        # Create temporal entanglement between forward and backward evolutions
        entangled_history = []
        for fwd, bwd in zip(field_history, backward_history):
            entangled, _ = temporal_entanglement(fwd, bwd, 0.3)
            entangled_history.append(entangled)
        
        # Store this iteration's results
        all_iterations.append({
            'forward': field_history,
            'backward': backward_history,
            'entangled': entangled_history,
            'times': time_points
        })
        
        # Use entangled history as the starting point for next iteration
        field.update_state(entangled_history[0], 0)
        
        # Compute temporal correlation for this iteration
        correlation = compute_temporal_correlation(entangled_history)
        print(f"  Temporal correlation: min={np.min(correlation):.3f}, max={np.max(correlation):.3f}")
    
    # Return final iteration results
    final_result = all_iterations[-1]
    final_result['all_iterations'] = all_iterations
    final_result['correlation'] = compute_temporal_correlation(final_result['entangled'])
    
    # Reset field to final entangled state
    field.update_state(final_result['entangled'][-1], 0)
    
    print(f"Bidirectional evolution complete. Field evolved to t={field.time:.3f}")
    return final_result


def visualize_temporal_correlation(correlation_matrix: np.ndarray,
                                  times: List[float],
                                  title: str = "Temporal Correlation Matrix",
                                  figsize: Tuple[int, int] = (10, 8)) -> None:
    """
    Visualize the temporal correlation matrix.
    
    Args:
        correlation_matrix: Correlation matrix from compute_temporal_correlation
        times: List of time points corresponding to matrix indices
        title: Plot title
        figsize: Figure size
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot correlation matrix as heatmap
    im = ax.imshow(correlation_matrix, cmap='coolwarm', vmin=-1, vmax=1, 
                  extent=[times[0], times[-1], times[-1], times[0]])
    
    # Add colorbar
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label('Correlation')
    
    # Set axis labels and title
    ax.set_xlabel('Time')
    ax.set_ylabel('Time')
    ax.set_title(title)
    
    # Add grid
    ax.grid(False)
    
    plt.tight_layout()
    return fig, ax
