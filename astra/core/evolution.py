"""
Field Evolution Module - Implementation of fKPZχ PDE dynamics

This module provides functions for evolving the QualiaField χ(x,t) according 
to the fractal Kardar-Parisi-Zhang-χ equation, a nonlinear stochastic PDE 
with a fractional Laplacian. It serves as the computational core of ASTRA.
"""

import numpy as np
from scipy.fft import fft2, ifft2, fftshift, ifftshift
from typing import Dict, List, Tuple, Any, Optional
import matplotlib.pyplot as plt

from .field import QualiaField


def fractional_laplacian_fft(field_state: np.ndarray, alpha: float = 1.5, 
                            dx: float = 1.0) -> np.ndarray:
    """
    Compute the fractional Laplacian using FFT:
    (-Δ)^(alpha/2) * f = IFFT( |k|^alpha * FFT(f) )
    
    This implements a spectral method for the fractional Laplacian by:
    1. Transforming the field to frequency space
    2. Multiplying by |k|^alpha
    3. Transforming back to real space
    
    Args:
        field_state: 2D array representing field values χ(x)
        alpha: Order of the fractional derivative (typically 1.0 to 2.0)
        dx: Grid spacing (assumed uniform)
        
    Returns:
        Array of same shape as field_state with fractional Laplacian applied
    """
    # Get field dimensions
    n_y, n_x = field_state.shape
    
    # Create frequency grid
    # We create the grid in a way that puts zero frequency at the center
    kx = 2 * np.pi * fftshift(np.fft.fftfreq(n_x, dx))
    ky = 2 * np.pi * fftshift(np.fft.fftfreq(n_y, dx))
    
    # Create 2D frequency grid using meshgrid
    kx_grid, ky_grid = np.meshgrid(kx, ky)
    
    # Calculate |k|^alpha = (kx^2 + ky^2)^(alpha/2)
    # Add a small epsilon to avoid division by zero at k=0
    epsilon = 1e-10
    k_squared = kx_grid**2 + ky_grid**2 + epsilon
    
    # Clamp k_squared to prevent excessive growth in high frequencies
    max_k_squared = 1000.0  # This limits the maximum frequency considered
    k_squared_clamped = np.clip(k_squared, 0, max_k_squared)
    k_magnitude_alpha = k_squared_clamped**(alpha/2)
    
    # Apply FFT to the field
    field_fft = fftshift(fft2(field_state))
    
    # Multiply by |k|^alpha in frequency space
    result_fft = field_fft * k_magnitude_alpha
    
    # Transform back to real space using inverse FFT
    # Take real part to eliminate small imaginary artifacts from numerical precision
    result = np.real(ifft2(ifftshift(result_fft)))
    
    # Clamp the final result as well
    max_result = 100.0
    return np.clip(result, -max_result, max_result)


def nonlinear_term(field_state: np.ndarray, lambda_param: float = 0.5,
                  gamma: float = 0.0) -> np.ndarray:
    """
    Compute the nonlinear term in the fKPZχ equation.
    
    For the MVP, we implement a simple quadratic nonlinearity scaled by lambda:
    λ * (∇χ)²
    
    The λ parameter (related to Sun position) controls the strength of nonlinearity.
    The γ parameter (related to Ascendant) introduces asymmetry.
    
    Args:
        field_state: Current field state
        lambda_param: Nonlinearity strength parameter (Sun)
        gamma: Symmetry-breaking parameter (Ascendant)
        
    Returns:
        Array with nonlinear term values
    """
    # Compute gradients using central difference
    dy, dx = np.gradient(field_state)
    
    # Compute (∇χ)²
    grad_squared = dx**2 + dy**2
    
    # Introduce asymmetry term if gamma != 0
    asymmetry = 0
    if gamma != 0:
        asymmetry = gamma * field_state**2
    
    # Scale by lambda parameter
    term = lambda_param * (grad_squared + asymmetry)
    
    # Clamp the term to prevent blow-up
    max_value = 100.0
    return np.clip(term, -max_value, max_value)


def noise_term(field_shape: Tuple[int, int], eta: float = 0.1, 
              noise_type: str = 'fractal', hurst: float = 0.8) -> np.ndarray:
    """
    Generate noise for the stochastic term.
    
    In ASTRA, the Moon is associated with the fractal noise generator η_f.
    
    This implementation provides two noise options:
    - 'gaussian': Simple white noise scaled by eta
    - 'fractal': Colored noise with spectrum |k|^(-2*hurst-1)
    
    Args:
        field_shape: Shape of the field (ny, nx)
        eta: Noise amplitude parameter (Moon)
        noise_type: Type of noise ('gaussian' or 'fractal')
        hurst: Hurst exponent for fractal noise (0.5=Brownian, >0.5=persistent)
        
    Returns:
        Noise field of specified shape
    """
    if noise_type == 'gaussian':
        # Simple Gaussian white noise
        return eta * np.random.randn(*field_shape)
    
    elif noise_type == 'fractal':
        # Fractal noise via spectral synthesis
        n_y, n_x = field_shape
        
        # Create frequency grid (centered)
        kx = 2 * np.pi * fftshift(np.fft.fftfreq(n_x))
        ky = 2 * np.pi * fftshift(np.fft.fftfreq(n_y))
        kx_grid, ky_grid = np.meshgrid(kx, ky)
        
        # Compute power spectrum |k|^(-2*hurst-1)
        # Add small epsilon to avoid division by zero at k=0
        epsilon = 1e-10
        k_magnitude = np.sqrt(kx_grid**2 + ky_grid**2 + epsilon)
        spectrum = k_magnitude**(-2*hurst-1)
        spectrum[0, 0] = 0  # Zero out DC component
        
        # Generate white noise in frequency domain with complex phases
        white_noise_real = np.random.randn(*field_shape)
        white_noise_imag = np.random.randn(*field_shape)
        white_noise_complex = fftshift(fft2(white_noise_real + 1j * white_noise_imag))
        
        # Color the noise by multiplying spectrum
        colored_noise_fft = white_noise_complex * np.sqrt(spectrum)
        
        # Transform back to real space
        colored_noise = np.real(ifft2(ifftshift(colored_noise_fft)))
        
        # Normalize and scale by eta
        colored_noise = colored_noise / np.std(colored_noise) * eta
        
        return colored_noise
    
    else:
        raise ValueError(f"Unknown noise type: {noise_type}")


def evolve_step(field: QualiaField, dt: float, 
               params: Optional[Dict[str, float]] = None) -> np.ndarray:
    """
    Evolve the QualiaField by one time step according to the fKPZχ equation.
    
    The full PDE has the form:
    ∂χ/∂t = -(-Δ)^(α/2)χ + λ(∇χ)² + η_f
    
    Where:
    - (-Δ)^(α/2) is the fractional Laplacian of order α
    - λ(∇χ)² is the nonlinear term scaled by λ (Sun parameter)
    - η_f is the fractal noise term scaled by η (Moon parameter)
    
    Args:
        field: The QualiaField object to evolve
        dt: Time step size
        params: Optional parameter dictionary to override field.params
        
    Returns:
        New field state after evolution
    """
    # Get current state
    current_state = field.get_state()
    
    # Get parameters (use provided or from field)
    if params is None:
        params = field.params
    
    # Extract parameters
    alpha = params.get('alpha', 1.5)
    lambda_param = params.get('lambda', 0.5)
    gamma = params.get('gamma', 0.0)
    eta = params.get('eta', 0.1)
    noise_type = params.get('noise_type', 'fractal')
    hurst = params.get('hurst', 0.8)
    
    # 1. Compute fractional Laplacian term (-(-Δ)^(α/2)χ)
    laplacian_term = -fractional_laplacian_fft(current_state, alpha)
    
    # 2. Compute nonlinear term (λ(∇χ)²)
    nonlin_term = nonlinear_term(current_state, lambda_param, gamma)
    
    # 3. Generate noise term (η_f)
    noise = noise_term(current_state.shape, eta, noise_type, hurst)
    
    # 4. Planetary perturbations (not implemented in MVP)
    # TODO: Add planetary perturbation terms from archetypes module
    perturbations = 0.0
    
    # Compute total derivative
    dfield_dt = laplacian_term + nonlin_term + noise + perturbations
    
    # Euler step: χ(t+dt) = χ(t) + dt * dχ/dt
    new_state = current_state + dt * dfield_dt
    
    # Clamp the final field values to prevent excessive growth
    max_field = 10.0  # Maximum allowed field magnitude
    return np.clip(new_state, -max_field, max_field)


def evolve_chart(field: QualiaField, duration: float, dt: Optional[float] = None,
                params: Optional[Dict[str, float]] = None, 
                store_frames: int = 10) -> Tuple[List[np.ndarray], List[float]]:
    """
    Evolve the qualia field for a specified duration.
    
    Args:
        field: Initialized QualiaField object
        duration: Total time to simulate
        dt: Time step size (if None, use field.params['dt'])
        params: Optional parameter dictionary to override field.params
        store_frames: Number of intermediate frames to store (in addition to start/end)
        
    Returns:
        Tuple of (field_history, time_points)
    """
    # Use default dt from field if not specified
    if dt is None:
        dt = field.params.get('dt', 0.01)
    
    # Calculate number of steps
    num_steps = int(duration / dt)
    print(f"Evolving chart for {duration} units with dt={dt} ({num_steps} steps)...")
    
    # Determine when to store frames
    if store_frames > 0:
        store_interval = max(1, num_steps // store_frames)
    else:
        store_interval = num_steps + 1  # Never store intermediate frames
    
    # Store initial state
    field_history = [field.get_state()]
    time_points = [field.time]
    
    # Evolution loop
    for step in range(num_steps):
        # Evolve one step
        new_state = evolve_step(field, dt, params)
        
        # Update field
        field.update_state(new_state, dt)
        
        # Store frame if it's time
        if (step + 1) % store_interval == 0 or step == num_steps - 1:
            field_history.append(field.get_state())
            time_points.append(field.time)
            
            # Print progress
            progress = (step + 1) / num_steps * 100
            print(f"  Progress: {progress:.1f}% (t={field.time:.2f})")
    
    print(f"Evolution complete. Field evolved to t={field.time:.3f}")
    return field_history, time_points


def visualize_evolution(field_history: List[np.ndarray], 
                       time_points: List[float],
                       title: str = "QualiaField χ(x,t) Evolution",
                       cmap: str = 'viridis',
                       figsize: Tuple[int, int] = (15, 10)) -> None:
    """
    Visualize the evolution of the field over time.
    
    Args:
        field_history: List of field states
        time_points: Corresponding time values
        title: Plot title
        cmap: Colormap to use
        figsize: Figure size
    """
    n_frames = len(field_history)
    
    # Determine grid layout
    cols = min(3, n_frames)
    rows = (n_frames + cols - 1) // cols
    
    # Create figure
    fig, axes = plt.subplots(rows, cols, figsize=figsize)
    if rows == 1 and cols == 1:
        axes = np.array([axes])  # Handle single subplot case
    axes = axes.flatten()
    
    # Determine global color scale
    vmin = min(np.min(f) for f in field_history)
    vmax = max(np.max(f) for f in field_history)
    
    # Plot each frame
    for i, (field, t) in enumerate(zip(field_history, time_points)):
        if i < len(axes):
            im = axes[i].imshow(field, origin='lower', cmap=cmap, 
                              interpolation='nearest', vmin=vmin, vmax=vmax)
            axes[i].set_title(f"t = {t:.2f}")
            axes[i].set_xticks([])
            axes[i].set_yticks([])
    
    # Hide unused subplots
    for i in range(n_frames, len(axes)):
        axes[i].axis('off')
    
    # Add colorbar
    fig.subplots_adjust(right=0.9)
    cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
    fig.colorbar(im, cax=cbar_ax, label='χ(x,t) magnitude')
    
    # Add overall title
    fig.suptitle(title, fontsize=16)
    plt.tight_layout(rect=[0, 0, 0.9, 0.95])
    plt.show()
