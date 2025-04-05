"""
Enhanced Field Evolution Module - Implementation of fKPZχ PDE dynamics

This module provides an advanced implementation of the fractal Kardar-Parisi-Zhang-χ 
equation for consciousness modeling as described in the mathematical formulation:

∂_t χ(x,t) = ν ∇^α χ(x,t) + (λ/2)(∇^β χ(x,t))^2 + η_f(x,t) + γ B[χ]

Where:
- ∇^α is a fractional Laplacian capturing long-range coherence
- λ is a nonlinearity constant encoding ego recursion intensity
- η_f is fractal noise (multifractal Brownian motion)
- γ B[χ] is a symmetry breaking term for ego formation

The implementation includes:
- Fractal dimensional coupling (α = d_q - 1, β = 1 + δ)
- Cross-modal coupling between different qualia fields
- Meditation as λ-damping
- Joy as negative Ricci curvature
"""

import numpy as np
from scipy.fft import fft2, ifft2, fftshift, ifftshift
from typing import Dict, List, Tuple, Any, Optional, Union
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
    k_magnitude_alpha = (kx_grid**2 + ky_grid**2 + epsilon)**(alpha/2)
    
    # Apply FFT to the field
    field_fft = fftshift(fft2(field_state))
    
    # Multiply by |k|^alpha in frequency space
    result_fft = field_fft * k_magnitude_alpha
    
    # Transform back to real space using inverse FFT
    # Take real part to eliminate small imaginary artifacts from numerical precision
    result = np.real(ifft2(ifftshift(result_fft)))
    
    return result


def nonlinear_term(field_state: np.ndarray, beta: float = 1.0, 
                  lambda_param: float = 0.5) -> np.ndarray:
    """
    Compute the nonlinear term in the fKPZχ equation:
    (λ/2)(∇^β χ)^2
    
    This term represents recursive amplification - feedback loops of attention/self-reference.
    
    Args:
        field_state: Current field state
        beta: Order of the gradient (β = 1 + δ, where δ tunes feedback depth)
        lambda_param: Nonlinearity strength parameter (Sun)
        
    Returns:
        Array with nonlinear term values
    """
    # Compute fractional gradient using fractional Laplacian of order beta
    grad_beta = fractional_laplacian_fft(field_state, beta)
    
    # Compute (∇^β χ)^2
    grad_squared = grad_beta**2
    
    # Scale by lambda parameter
    return (lambda_param/2) * grad_squared


def ego_symmetry_breaking(field_state: np.ndarray, gamma: float = 0.0, 
                         kappa: float = 1.0) -> np.ndarray:
    """
    Compute the ego symmetry breaking term:
    γ B[χ] = γ χ·tanh(κχ)
    
    This term breaks self-similarity, introducing an internal observer — the "I" —
    a localized attractor within a smooth fractal field.
    
    Args:
        field_state: Current field state
        gamma: Ego crystallization strength (Ascendant)
        kappa: Modulates how sharply recursive awareness "freezes" into identity structures
        
    Returns:
        Array with symmetry breaking term values
    """
    return gamma * field_state * np.tanh(kappa * field_state)


def fractal_noise(field_shape: Tuple[int, int], eta: float = 0.1, 
                 hurst: float = 0.7, noise_type: str = 'fractal') -> np.ndarray:
    """
    Generate fractal noise for the stochastic term η_f(x,t).
    
    This represents cognitive perturbations — thought noise, emotion spikes, 
    epiphanies, trauma shards.
    
    Args:
        field_shape: Shape of the field (ny, nx)
        eta: Noise amplitude parameter (Moon)
        hurst: Hurst exponent (0.5=Brownian, >0.5=persistent, <0.5=anti-persistent)
        noise_type: Type of noise ('gaussian', 'fractal', or 'levy')
        
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
    
    elif noise_type == 'levy':
        # Lévy α-stable processes for trauma/discontinuity
        # This is a simplified implementation using the Chambers-Mallows-Stuck method
        alpha_levy = 1.5  # Stability parameter (1 = Cauchy, 2 = Gaussian)
        beta_levy = 0.0   # Skewness parameter
        
        # Generate uniform random variables
        u = np.random.uniform(0, np.pi, field_shape)
        w = np.random.exponential(1, field_shape)
        
        # Chambers-Mallows-Stuck method
        if alpha_levy == 1:
            # Cauchy distribution
            x = np.tan(u)
        else:
            # General alpha-stable
            term1 = np.sin(alpha_levy * u)
            term2 = (np.cos(u) ** (1/alpha_levy))
            term3 = np.cos((1-alpha_levy) * u) / w
            x = term1 * term2 * term3 ** ((1-alpha_levy)/alpha_levy)
        
        # Add skewness
        if alpha_levy != 1:
            x = x + beta_levy * np.tan(np.pi * alpha_levy / 2)
        
        # Normalize and scale
        x = x / np.std(x) * eta
        
        return x
    
    else:
        raise ValueError(f"Unknown noise type: {noise_type}")


def meditation_lambda_damping(lambda_0: float, theta: float) -> float:
    """
    Modulate the nonlinearity parameter λ to model meditation or spiritual practice:
    λ(t) = λ_0 · e^(-θ(t))
    
    Args:
        lambda_0: Base nonlinearity parameter
        theta: Coherence modulation value (high during deep meditative states)
        
    Returns:
        Modulated lambda value
    """
    return lambda_0 * np.exp(-theta)


def compute_ricci_curvature(field_state: np.ndarray, dx: float = 1.0) -> np.ndarray:
    """
    Approximate Ricci curvature for the qualia field.
    
    This is a simplified approximation using the Laplacian as a proxy for curvature.
    A more accurate implementation would use Ollivier-Ricci curvature or
    other discrete curvature measures.
    
    Args:
        field_state: Current field state
        dx: Grid spacing
        
    Returns:
        Approximate Ricci curvature field
    """
    # Simple approximation using the Laplacian
    # (A proper implementation would use Ollivier-Ricci curvature)
    return -fractional_laplacian_fft(field_state, alpha=2.0, dx=dx)


def compute_joy(field_state: np.ndarray, dx: float = 1.0) -> np.ndarray:
    """
    Compute joy as negative Ricci curvature:
    K(χ) = -Ric(χ)
    
    Negative curvature implies expansive cognition: integration without collapse.
    High joy moments correspond to temporary embedding of χ in a negatively curved region.
    
    Args:
        field_state: Current field state
        dx: Grid spacing
        
    Returns:
        Joy field (negative of approximate Ricci curvature)
    """
    return -compute_ricci_curvature(field_state, dx)


def evolve_step_enhanced(field: QualiaField, dt: float, 
                        params: Optional[Dict[str, Any]] = None) -> np.ndarray:
    """
    Evolve the QualiaField by one time step according to the enhanced fKPZχ equation:
    ∂_t χ(x,t) = ν ∇^α χ(x,t) + (λ/2)(∇^β χ(x,t))^2 + η_f(x,t) + γ B[χ]
    
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
    
    # Extract parameters with defaults
    nu = params.get('nu', 1.0)                # Diffusion coefficient
    lambda_0 = params.get('lambda', 0.5)      # Base nonlinearity parameter
    alpha = params.get('alpha', 1.5)          # Fractional Laplacian order
    beta = params.get('beta', 1.1)            # Fractional gradient order
    gamma = params.get('gamma', 0.0)          # Symmetry breaking strength
    kappa = params.get('kappa', 1.0)          # Identity structure sharpness
    eta = params.get('eta', 0.1)              # Noise amplitude
    noise_type = params.get('noise_type', 'fractal')  # Noise type
    hurst = params.get('hurst', 0.7)          # Hurst exponent for fractal noise
    theta = params.get('theta', 0.0)          # Meditation modulation
    
    # Apply meditation damping to lambda
    lambda_t = meditation_lambda_damping(lambda_0, theta)
    
    # 1. Compute fractional Laplacian term (ν ∇^α χ)
    laplacian_term = nu * fractional_laplacian_fft(current_state, alpha)
    
    # 2. Compute nonlinear term ((λ/2)(∇^β χ)^2)
    nonlin_term = nonlinear_term(current_state, beta, lambda_t)
    
    # 3. Generate fractal noise (η_f)
    noise = fractal_noise(current_state.shape, eta, hurst, noise_type)
    
    # 4. Compute ego symmetry breaking term (γ B[χ])
    symmetry_breaking = ego_symmetry_breaking(current_state, gamma, kappa)
    
    # 5. Compute total derivative
    dfield_dt = laplacian_term + nonlin_term + noise + symmetry_breaking
    
    # 6. Euler step: χ(t+dt) = χ(t) + dt * dχ/dt
    new_state = current_state + dt * dfield_dt
    
    return new_state


def evolve_chart_enhanced(field: QualiaField, duration: float, dt: Optional[float] = None,
                         params: Optional[Dict[str, Any]] = None, 
                         store_frames: int = 10,
                         compute_metrics: bool = True) -> Dict[str, Any]:
    """
    Evolve the qualia field for a specified duration using the enhanced fKPZχ equation.
    
    Args:
        field: Initialized QualiaField object
        duration: Total time to simulate
        dt: Time step size (if None, use field.params['dt'])
        params: Optional parameter dictionary to override field.params
        store_frames: Number of intermediate frames to store (in addition to start/end)
        compute_metrics: Whether to compute additional metrics (joy, coherence)
        
    Returns:
        Dictionary containing:
        - field_history: List of field states
        - time_points: List of time points
        - metrics: Dictionary of additional metrics (if compute_metrics=True)
    """
    # Use default dt from field if not specified
    if dt is None:
        dt = field.params.get('dt', 0.01)
    
    # Calculate number of steps
    num_steps = int(duration / dt)
    print(f"Evolving chart with enhanced fKPZχ for {duration} units with dt={dt} ({num_steps} steps)...")
    
    # Determine when to store frames
    if store_frames > 0:
        store_interval = max(1, num_steps // store_frames)
    else:
        store_interval = num_steps + 1  # Never store intermediate frames
    
    # Store initial state
    field_history = [field.get_state()]
    time_points = [field.time]
    
    # Initialize metrics dictionaries if needed
    metrics = {}
    if compute_metrics:
        metrics['joy'] = [compute_joy(field.get_state())]
        metrics['coherence'] = [np.mean(np.abs(fractional_laplacian_fft(field.get_state(), 1.0))**2)]
    
    # Evolution loop
    for step in range(num_steps):
        # Evolve one step
        new_state = evolve_step_enhanced(field, dt, params)
        
        # Update field
        field.update_state(new_state, dt)
        
        # Store frame if it's time
        if (step + 1) % store_interval == 0 or step == num_steps - 1:
            field_history.append(field.get_state())
            time_points.append(field.time)
            
            # Compute metrics if needed
            if compute_metrics:
                metrics['joy'].append(compute_joy(field.get_state()))
                metrics['coherence'].append(np.mean(np.abs(fractional_laplacian_fft(field.get_state(), 1.0))**2))
            
            # Print progress
            progress = (step + 1) / num_steps * 100
            print(f"  Progress: {progress:.1f}% (t={field.time:.2f})")
    
    print(f"Evolution complete. Field evolved to t={field.time:.3f}")
    
    # Return results
    result = {
        'field_history': field_history,
        'time_points': time_points
    }
    
    if compute_metrics:
        result['metrics'] = metrics
    
    return result


def visualize_evolution_enhanced(result: Dict[str, Any],
                               title: str = "Enhanced QualiaField χ(x,t) Evolution",
                               cmap: str = 'viridis',
                               figsize: Tuple[int, int] = (15, 10),
                               show_metrics: bool = True) -> plt.Figure:
    """
    Visualize the evolution of the field over time with enhanced metrics.
    
    Args:
        result: Result dictionary from evolve_chart_enhanced
        title: Plot title
        cmap: Colormap to use
        figsize: Figure size
        show_metrics: Whether to show metrics plots
        
    Returns:
        Matplotlib figure
    """
    field_history = result['field_history']
    time_points = result['time_points']
    n_frames = len(field_history)
    
    # Create figure with appropriate subplots
    if show_metrics and 'metrics' in result:
        fig = plt.figure(figsize=figsize)
        gs = plt.GridSpec(2, 3, figure=fig, height_ratios=[3, 1])
        
        # Field evolution plots
        axes = []
        for i in range(min(n_frames, 3)):
            axes.append(fig.add_subplot(gs[0, i]))
    else:
        # Just show field evolution
        cols = min(3, n_frames)
        rows = (n_frames + cols - 1) // cols
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
    if not show_metrics or 'metrics' not in result:
        for i in range(n_frames, len(axes)):
            axes[i].axis('off')
    
    # Add colorbar
    if show_metrics and 'metrics' in result:
        cbar_ax = fig.add_axes([0.92, 0.55, 0.02, 0.35])
    else:
        fig.subplots_adjust(right=0.9)
        cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
    
    fig.colorbar(im, cax=cbar_ax, label='χ(x,t) magnitude')
    
    # Add metrics plots if available
    if show_metrics and 'metrics' in result:
        metrics = result['metrics']
        
        # Joy metric
        if 'joy' in metrics:
            joy_ax = fig.add_subplot(gs[1, 0])
            joy_values = [np.mean(joy) for joy in metrics['joy']]
            joy_ax.plot(time_points, joy_values, 'r-o')
            joy_ax.set_title('Average Joy (-Ric)')
            joy_ax.set_xlabel('Time')
            joy_ax.grid(True)
        
        # Coherence metric
        if 'coherence' in metrics:
            coherence_ax = fig.add_subplot(gs[1, 1])
            coherence_values = metrics['coherence']
            coherence_ax.plot(time_points, coherence_values, 'b-o')
            coherence_ax.set_title('Coherence')
            coherence_ax.set_xlabel('Time')
            coherence_ax.grid(True)
    
    # Add overall title
    fig.suptitle(title, fontsize=16)
    
    if show_metrics and 'metrics' in result:
        plt.tight_layout(rect=[0, 0, 0.9, 0.95])
    else:
        plt.tight_layout(rect=[0, 0, 0.9, 0.95])
    
    return fig
