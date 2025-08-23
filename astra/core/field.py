"""
Qualia Field Implementation - Core of the χ-Layer

This module implements the QualiaField class which represents the
dynamically evolving psychological field (χ(x,t)) at the heart of ASTRA.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, Dict, Any, Optional


class QualiaField:
    """
    The QualiaField represents the qualia surface χ(x,t) that evolves according to 
    the fKPZχ equation in ASTRA.
    
    This field encodes the psychological/archetypal state space, initialized from 
    natal chart data and evolved via a fractional PDE system with planetary operators.
    """
    
    def __init__(self, 
                 natal_data: Any, 
                 grid_size: Tuple[int, int] = (64, 64), 
                 boundary: str = 'periodic',
                 initial_noise_scale: float = 0.1):
        """
        Initialize a new QualiaField from natal chart data.
        
        Args:
            natal_data: AstrologicalSubject from Kerykeion containing natal chart data
            grid_size: Dimensions of the 2D qualia field (default: 64x64)
            boundary: Boundary condition type ('periodic', 'reflective', etc.)
            initial_noise_scale: Scale of random fluctuations in initial state
        """
        # Core field properties
        self.grid_size = grid_size
        self.state = np.zeros(grid_size)  # χ(x,t=0) - The qualia surface
        self.time = 0.0  # Current simulation time
        self.boundary = boundary
        
        # Store natal data
        self.natal_data = natal_data
        
        # Parameters derived from chart - will be refined in future versions
        # Related to README concepts:
        # * Sun = nonlinearity parameter λ
        # * Moon = fractal noise generator η_f
        # * Ascendant = symmetry-breaking γ
        self.params = self._derive_params_from_chart()
        
        # Initialize the field state based on chart data
        self._initialize_from_natal(initial_noise_scale)
        
        # Store evolution history
        self.history = [self.state.copy()]
        self.time_points = [self.time]
        
        print(f"Initialized QualiaField (χ-Layer) with size {grid_size}")
        print(f"Derived parameters: {self.params}")

    def _derive_params_from_chart(self) -> Dict[str, float]:
        """
        Derive system parameters from the natal chart data.
        
        In the MVP, implements simplified parameter mapping:
        * Sun position → nonlinearity (λ)
        * Moon position → noise scale (η)
        * Ascendant position → symmetry parameter (γ)
        
        Returns:
            Dictionary of parameters for the fKPZχ evolution
        """
        # Extract relevant positions
        try:
            sun_pos = self.natal_data.sun['abs_pos'] / 360.0  # Normalize to [0,1]
            moon_pos = self.natal_data.moon['abs_pos'] / 360.0  # Normalize to [0,1]
            asc_pos = self.natal_data.first_house['abs_pos'] / 360.0  # Normalize to [0,1]
            
            # Map to parameter ranges - these mappings are simplified for MVP
            # Will be refined based on astrological significance in later versions
            lambda_param = 0.1 + 0.9 * sun_pos  # Nonlinearity: 0.1 to 1.0
            eta_param = 0.05 + 0.2 * moon_pos   # Noise: 0.05 to 0.25
            gamma_param = -0.5 + asc_pos        # Symmetry: -0.5 to 0.5
            
            # Fractional Laplacian order - could be linked to other factors
            alpha_param = 1.5  # Standard choice between 1 and 2
            
            return {
                'lambda': lambda_param,  # Nonlinearity (Sun)
                'eta': eta_param,        # Noise scale (Moon)
                'gamma': gamma_param,    # Symmetry breaking (Ascendant)
                'alpha': alpha_param,    # Fractional Laplacian order
                'dt': 0.01               # Default time step
            }
            
        except (AttributeError, KeyError) as e:
            print(f"Warning: Error deriving params from chart: {e}")
            # Fallback to defaults
            return {
                'lambda': 0.5,
                'eta': 0.1,
                'gamma': 0.0,
                'alpha': 1.5,
                'dt': 0.01
            }

    def _initialize_from_natal(self, noise_scale: float = 0.1):
        """
        Initialize the field based on natal chart data.
        
        In the MVP, we place Gaussian peaks for major planets and
        add background noise.
        
        Args:
            noise_scale: Scale of random noise to add
        """
        # Initialize with small random noise
        self.state = noise_scale * np.random.randn(*self.grid_size)
        
        # Define center and width for peaks
        center_x, center_y = np.array(self.grid_size) // 2
        width_x = self.grid_size[0] // 8
        width_y = self.grid_size[1] // 8
        
        # Create coordinate grid for vectorized calculations
        y_coords, x_coords = np.mgrid[0:self.grid_size[0], 0:self.grid_size[1]]
        
        # Add peaks for major celestial bodies
        planets = [
            ('sun', 1.0),  # (planet_key, amplitude)
            ('moon', 0.8),
            ('mercury', 0.6),
            ('venus', 0.7),
            ('mars', 0.65),
            ('jupiter', 0.75),
            ('saturn', 0.7),
            ('uranus', 0.5),
            ('neptune', 0.5),
            ('pluto', 0.45)
        ]
        
        for planet_key, amplitude in planets:
            try:
                # Get position and map to grid
                planet_data = getattr(self.natal_data, planet_key)
                pos_angle = planet_data['abs_pos']
                
                # Map 0-360° to position on grid perimeter (simplified)
                # This creates a radial layout where planets are distributed
                # around the field according to their zodiacal positions
                theta = np.deg2rad(pos_angle)
                radius = min(center_x, center_y) * 0.8  # 80% to edge
                
                x_pos = center_x + int(radius * np.cos(theta))
                y_pos = center_y + int(radius * np.sin(theta))
                
                # Ensure within grid
                x_pos = max(0, min(x_pos, self.grid_size[1]-1))
                y_pos = max(0, min(y_pos, self.grid_size[0]-1))
                
                # Add Gaussian peak
                gauss_peak = amplitude * np.exp(
                    -((x_coords - x_pos)**2 / (2*width_x**2) + 
                      (y_coords - y_pos)**2 / (2*width_y**2))
                )
                self.state += gauss_peak
                
                print(f"Added {planet_key} influence at ({x_pos},{y_pos})")
                
            except (AttributeError, KeyError) as e:
                print(f"Warning: Could not add {planet_key}: {e}")
        
        # Normalize to [-1, 1] if the field has any variation. The previous
        # implementation attempted to shift the range using ``* 2 - 1``, which
        # actually produced values in ``[-3, 1]`` and triggered a division by
        # zero when the field was entirely flat. We instead scale by the maximum
        # absolute value only when it is non-zero, leaving a zero field
        # unchanged.
        max_val = np.max(np.abs(self.state))
        if max_val > 0:
            self.state = self.state / max_val
    
    def get_state(self) -> np.ndarray:
        """
        Return the current field state χ(x,t).
        
        Returns:
            Current 2D state array
        """
        return self.state.copy()
    
    def update_state(self, new_state: np.ndarray, dt: float):
        """
        Update the field to a new state and increment time.
        
        Args:
            new_state: New field values to set
            dt: Time step size
        """
        self.state = new_state.copy()
        self.time += dt
        
        # Optionally store in history
        self.history.append(self.state.copy())
        self.time_points.append(self.time)
    
    def visualize(self, ax=None, show=True, cmap='viridis', 
                  title: Optional[str] = None):
        """
        Create a visualization of the current field state.
        
        Args:
            ax: Optional matplotlib Axes for plotting
            show: Whether to call plt.show()
            cmap: Colormap to use
            title: Optional title; defaults to time info
            
        Returns:
            Matplotlib figure and axes objects
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 8))
        else:
            fig = ax.figure
            
        # Plot the field
        im = ax.imshow(self.state, cmap=cmap, origin='lower', 
                       interpolation='nearest')
        
        # Add colorbar
        fig.colorbar(im, ax=ax, label='χ(x,t) magnitude')
        
        # Add title
        if title is None:
            title = f"QualiaField χ(x,t) at t={self.time:.2f}"
        ax.set_title(title)
        
        if show:
            plt.tight_layout()
            plt.show()
            
        return fig, ax
