"""
Threshold Detection Module for ASTRA

This module detects significant transitions and threshold crossings in the qualia field.
It provides tools for:
- Detecting when field values cross predefined thresholds
- Identifying phase transitions in field dynamics
- Tracking significant changes in topological features
"""

import numpy as np
from typing import Dict, List, Tuple, Any, Optional, Union
from enum import Enum, auto
from datetime import datetime

from .narrative import NarrativeEvent, EventType


class ThresholdType(Enum):
    """Types of thresholds that can be detected in the qualia field."""
    VALUE = auto()           # Raw field value threshold
    GRADIENT = auto()        # Field gradient threshold
    TOPOLOGY = auto()        # Topological feature threshold
    CURVATURE = auto()       # Ricci curvature threshold
    ENTROPY = auto()         # Field entropy threshold
    COMPLEXITY = auto()      # Complexity measure threshold
    RESONANCE = auto()       # Resonance between field regions
    COHERENCE = auto()       # Field coherence threshold


class ThresholdEvent:
    """
    Represents a threshold crossing event in the qualia field.
    
    Attributes:
        timestamp: When the threshold was crossed
        threshold_type: Type of threshold
        threshold_value: Value of the threshold
        field_value: Actual field value at crossing
        description: Human-readable description
        location: Coordinates where threshold was crossed
        metadata: Additional event-specific data
    """
    
    def __init__(self,
                timestamp: float,
                threshold_type: ThresholdType,
                threshold_value: float,
                field_value: float,
                description: str,
                location: Optional[Tuple[int, int]] = None,
                metadata: Optional[Dict[str, Any]] = None):
        """Initialize a threshold event."""
        self.timestamp = timestamp
        self.threshold_type = threshold_type
        self.threshold_value = threshold_value
        self.field_value = field_value
        self.description = description
        self.location = location
        self.metadata = metadata or {}
        self.crossed_upward = field_value > threshold_value
        self.real_time = datetime.now()
    
    def to_narrative_event(self) -> NarrativeEvent:
        """Convert threshold event to narrative event."""
        # Determine event type based on threshold type
        event_type_map = {
            ThresholdType.VALUE: EventType.THRESHOLD,
            ThresholdType.GRADIENT: EventType.TRANSFORMATION,
            ThresholdType.TOPOLOGY: EventType.EMERGENCE,
            ThresholdType.CURVATURE: EventType.INSIGHT,
            ThresholdType.ENTROPY: EventType.DISSOLUTION,
            ThresholdType.COMPLEXITY: EventType.BIFURCATION,
            ThresholdType.RESONANCE: EventType.RESONANCE,
            ThresholdType.COHERENCE: EventType.INTEGRATION
        }
        
        event_type = event_type_map.get(self.threshold_type, EventType.THRESHOLD)
        
        # Calculate intensity based on how far beyond threshold
        if self.crossed_upward:
            intensity = min(1.0, (self.field_value - self.threshold_value) / self.threshold_value)
        else:
            intensity = min(1.0, (self.threshold_value - self.field_value) / self.threshold_value)
        
        # Create narrative event
        return NarrativeEvent(
            timestamp=self.timestamp,
            event_type=event_type,
            description=self.description,
            intensity=intensity,
            location=self.location,
            metadata={
                'threshold_type': self.threshold_type.name,
                'threshold_value': self.threshold_value,
                'field_value': self.field_value,
                'crossed_upward': self.crossed_upward,
                **self.metadata
            }
        )
    
    def __str__(self) -> str:
        """String representation of the threshold event."""
        direction = "↑" if self.crossed_upward else "↓"
        return f"[{self.timestamp:.2f}] {self.threshold_type.name} {direction}: {self.description}"


def detect_threshold_crossings(current_field: np.ndarray,
                              previous_field: Optional[np.ndarray] = None,
                              timestamp: float = 0.0,
                              thresholds: Optional[Dict[str, float]] = None) -> List[ThresholdEvent]:
    """
    Detect threshold crossings in the qualia field.
    
    Args:
        current_field: Current qualia field state
        previous_field: Previous field state (for detecting changes)
        timestamp: Current simulation time
        thresholds: Dictionary of threshold values to check
        
    Returns:
        List of threshold events
    """
    events = []
    
    # Default thresholds if none provided
    if thresholds is None:
        thresholds = {
            'value_high': 0.8,           # High absolute value
            'value_low': 0.2,            # Low absolute value
            'gradient_high': 0.3,        # High gradient
            'entropy_high': 0.7,         # High entropy
            'complexity_high': 0.6,      # High complexity
            'coherence_high': 0.8        # High coherence
        }
    
    # Normalize field to [0,1] for consistent thresholds
    field_min = np.min(current_field)
    field_max = np.max(current_field)
    if field_max > field_min:
        normalized_field = (current_field - field_min) / (field_max - field_min)
    else:
        normalized_field = np.zeros_like(current_field)
    
    # Check for high value threshold crossings
    high_value_mask = normalized_field > thresholds['value_high']
    if np.any(high_value_mask):
        # Find the location of maximum value
        max_loc = np.unravel_index(np.argmax(normalized_field), normalized_field.shape)
        max_val = normalized_field[max_loc]
        
        events.append(ThresholdEvent(
            timestamp=timestamp,
            threshold_type=ThresholdType.VALUE,
            threshold_value=thresholds['value_high'],
            field_value=max_val,
            description=f"Field value exceeds high threshold ({max_val:.2f} > {thresholds['value_high']:.2f})",
            location=max_loc
        ))
    
    # Check for low value threshold crossings
    low_value_mask = normalized_field < thresholds['value_low']
    if np.any(low_value_mask):
        # Find the location of minimum value
        min_loc = np.unravel_index(np.argmin(normalized_field), normalized_field.shape)
        min_val = normalized_field[min_loc]
        
        events.append(ThresholdEvent(
            timestamp=timestamp,
            threshold_type=ThresholdType.VALUE,
            threshold_value=thresholds['value_low'],
            field_value=min_val,
            description=f"Field value falls below low threshold ({min_val:.2f} < {thresholds['value_low']:.2f})",
            location=min_loc
        ))
    
    # Check for gradient threshold crossings if previous field is available
    if previous_field is not None:
        # Normalize previous field
        prev_min = np.min(previous_field)
        prev_max = np.max(previous_field)
        if prev_max > prev_min:
            normalized_prev = (previous_field - prev_min) / (prev_max - prev_min)
        else:
            normalized_prev = np.zeros_like(previous_field)
        
        # Calculate gradient (change)
        gradient = np.abs(normalized_field - normalized_prev)
        
        # Check for high gradient
        high_gradient_mask = gradient > thresholds['gradient_high']
        if np.any(high_gradient_mask):
            # Find location of maximum gradient
            max_grad_loc = np.unravel_index(np.argmax(gradient), gradient.shape)
            max_grad = gradient[max_grad_loc]
            
            events.append(ThresholdEvent(
                timestamp=timestamp,
                threshold_type=ThresholdType.GRADIENT,
                threshold_value=thresholds['gradient_high'],
                field_value=max_grad,
                description=f"Field gradient exceeds threshold ({max_grad:.2f} > {thresholds['gradient_high']:.2f})",
                location=max_grad_loc
            ))
    
    # Calculate entropy (as a measure of disorder/complexity)
    # Use histogram-based entropy estimation
    hist, _ = np.histogram(normalized_field, bins=20, range=(0, 1), density=True)
    hist = hist[hist > 0]  # Remove zeros
    entropy = -np.sum(hist * np.log2(hist)) / np.log2(len(hist))  # Normalized entropy
    
    # Check entropy threshold
    if entropy > thresholds['entropy_high']:
        events.append(ThresholdEvent(
            timestamp=timestamp,
            threshold_type=ThresholdType.ENTROPY,
            threshold_value=thresholds['entropy_high'],
            field_value=entropy,
            description=f"Field entropy exceeds threshold ({entropy:.2f} > {thresholds['entropy_high']:.2f})"
        ))
    
    # Calculate field coherence (spatial autocorrelation)
    # Simple measure: ratio of mean to standard deviation
    if np.std(normalized_field) > 0:
        coherence = np.mean(normalized_field) / np.std(normalized_field)
        
        # Normalize coherence to [0,1] range (approximately)
        coherence = min(1.0, coherence / 5.0)
        
        # Check coherence threshold
        if coherence > thresholds['coherence_high']:
            events.append(ThresholdEvent(
                timestamp=timestamp,
                threshold_type=ThresholdType.COHERENCE,
                threshold_value=thresholds['coherence_high'],
                field_value=coherence,
                description=f"Field coherence exceeds threshold ({coherence:.2f} > {thresholds['coherence_high']:.2f})"
            ))
    
    return events


def detect_phase_transitions(field_history: List[np.ndarray],
                            timestamps: List[float],
                            window_size: int = 5) -> List[ThresholdEvent]:
    """
    Detect phase transitions in the evolution of the qualia field.
    
    A phase transition is a significant change in the qualitative behavior
    of the field, such as a shift from ordered to chaotic dynamics.
    
    Args:
        field_history: List of field states over time
        timestamps: Corresponding timestamps for each field state
        window_size: Size of window for detecting transitions
        
    Returns:
        List of threshold events representing phase transitions
    """
    if len(field_history) < window_size + 1:
        return []  # Not enough history to detect transitions
    
    events = []
    
    # Calculate complexity measure for each field state
    # (using entropy as a simple complexity measure)
    complexity_values = []
    
    for field in field_history:
        # Normalize field
        field_min = np.min(field)
        field_max = np.max(field)
        if field_max > field_min:
            normalized = (field - field_min) / (field_max - field_min)
        else:
            normalized = np.zeros_like(field)
        
        # Calculate entropy
        hist, _ = np.histogram(normalized, bins=20, range=(0, 1), density=True)
        hist = hist[hist > 0]  # Remove zeros
        entropy = -np.sum(hist * np.log2(hist)) / np.log2(len(hist))
        
        complexity_values.append(entropy)
    
    # Detect significant changes in complexity
    for i in range(window_size, len(complexity_values)):
        # Calculate mean and std of complexity in window
        window = complexity_values[i-window_size:i]
        window_mean = np.mean(window)
        window_std = np.std(window)
        
        # Current complexity
        current = complexity_values[i]
        
        # Check if current complexity is significantly different from window
        if window_std > 0 and abs(current - window_mean) > 2 * window_std:
            # This is a significant change - potential phase transition
            events.append(ThresholdEvent(
                timestamp=timestamps[i],
                threshold_type=ThresholdType.COMPLEXITY,
                threshold_value=window_mean + 2 * window_std if current > window_mean else window_mean - 2 * window_std,
                field_value=current,
                description=f"Phase transition detected: significant change in field complexity",
                metadata={
                    'previous_complexity': window_mean,
                    'complexity_change': current - window_mean,
                    'significance': abs(current - window_mean) / window_std
                }
            ))
    
    return events
