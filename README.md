# ASTRA: Archetypal Spacetime Tensor Resonance Architecture 🌌🧠

*Chart the shape of your psyche. Not as fate—but as resonance.* ✨

ASTRA is a modular, symbolic-quantitative system for modeling consciousness as a dynamic field. It reframes astrology as an ancient UI for **qualia topology** and formalizes it through fractal PDEs, topological data analysis, and planetary operator dynamics. 🌠🔬

## Table of Contents 📋

* Overview
* Architecture
* Installation
* Quickstart
* Web Interface
* Modules
* Testing Framework
* Development Roadmap
* License

## Overview 🚀

ASTRA is not astrology. 

It is **consciousness cartography** — a simulator for the evolving topological field of the psyche. ASTRA reinterprets planetary motion and symbolic archetypes as tensor perturbations on a nonlinear qualia surface. 🌈🧮

Given natal data, ASTRA:
1. ✅ Initializes a qualia field χ(x,0) from birth chart data
2. ✅ Evolves the field via fKPZχ PDEs with fractal noise
3. ✅ Models ego formation through symmetry breaking
4. ✅ Analyzes field topology (Betti numbers, Ricci curvature)
5. ✅ Generates symbolic narratives and archetypal event logs

## Architecture 🏗️

**Note**: The χ-Layer described here is the explicit implementation of the Quantum-State Modeling referenced in the Quantum Astrology PRD. Rather than representing consciousness as a static Hilbert vector, ASTRA models it as a dynamically evolving qualia field, where planetary archetypes act as tensor perturbations and recursive symbolic dynamics emerge through PDE-driven attractor states. fKPZχ thus functions as a recursive quantum-like state engine operating over psychological topologies.

ASTRA is organized in **recursive layers**:

### χ-Layer: Field Evolution 🌊

* fKPZχ core PDE engine
* Fractional Laplacian (FFT accelerated)
* Moon = fractal noise generator η_f
* Ascendant = symmetry-breaking γ
* Sun = nonlinearity parameter λ

### 𝒸-Layer: Archetypal Operators 🌍
* Planets as tensor fields modulating χ
* Aspect matrix μ_ij (cross-modal coupling)
* Phase-transition triggers (e.g., Pluto λ → ∞)

### 𝓈-Layer: Topological Signature 🔍
* Persistent homology (Betti loops)
* Ollivier-Ricci curvature
* Detection of aspects as topological motifs

### 𝓂-Layer: Symbolic Narrative 📖
* Event log generator:
   * `PLUTO_RECURSIVE_CATHARSIS`
   * `VENUS_POSITIVE_CURVATURE`
   * `SATURN_EGO_CONDENSATION`

### Visualization Layer 🖥️

* AstroChart: orbital harmony viewer
* Field Viewer: live evolution of χ(x,t)
* Betti overlays & event stream timeline

## Installation (Planned) 🛠️

```bash
# Clone the repo
git clone https://github.com/yourname/astra.git
cd astra

# Set up Python environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Install frontend deps (React)
cd frontend
npm install
```

## Quickstart 🚀

```python
# Import ASTRA components
from astra.core import QualiaField, evolve_chart
from astra.topology import compute_persistence_diagram, compute_joy_field

# Create chart with Kerykeion
from kerykeion import AstrologicalSubject
subject = AstrologicalSubject("Example Person", 1985, 1, 4, 5, 0, "Minneapolis", "US")

# Initialize qualia field from chart
field = QualiaField(subject, grid_size=(128, 128))

# Evolve field via fKPZχ equation
result = evolve_chart(field, duration=2.0, dt=0.01, store_frames=5)

# Analyze field topology
final_state = result['field_history'][-1]
persistence = compute_persistence_diagram(final_state)
betti = compute_betti_numbers(persistence['diagrams'])
joy = compute_joy_field(final_state)

print(f"Betti numbers: β₀={betti[0]}, β₁={betti[1]}, β₂={betti[2]}")
```

## Web Interface 🌐

ASTRA includes a web interface built with HTML, CSS, and JavaScript that can be deployed on GitHub Pages.

### Features

* Birth data input form
* QualiaField visualization
* Topological analysis display
* Narrative event generation
* Interactive results dashboard

### Accessing the Web Interface

The ASTRA web interface is deployed at: https://prometheuswaluigi.github.io/ASTRA/

### Setting Up Google Places API

ASTRA uses the Google Places API for city autocomplete functionality. To set this up:

1. Obtain a Google Places API key from the [Google Cloud Console](https://console.cloud.google.com/)
2. Add the API key as a GitHub Secret named `GOOGLE_API_KEY` in your repository settings:
   - Go to your GitHub repository
   - Click on "Settings" > "Secrets and variables" > "Actions"
   - Click "New repository secret"
   - Name: `GOOGLE_API_KEY`
   - Value: Your Google Places API key
   - Click "Add secret"
3. The GitHub Action workflow will automatically inject this key when deploying to GitHub Pages

### Local Development

To run the web interface locally:

```bash
# Navigate to docs directory
cd docs

# If you have Python installed
python -m http.server 8000

# Then open http://localhost:8000 in your browser
```

The web interface provides a simple way to interact with ASTRA without needing to install all the dependencies or run Python code directly.

### Simple Input Page

If the main interface is too feature-rich or requires external API keys, a minimal fallback is available at [`docs/simple.html`](docs/simple.html).
It offers a basic form with name, birth date, time, and city fields using the built-in city database and displays a lightweight analysis without any additional setup.

## Modules 🧩

### `/core` ✅

* `QualiaField` - Field class representing χ(x,t)
* `evolve_chart()` - Evolution via fKPZχ equation
* `fractional_laplacian_fft()` - FFT-based implementation
* `nonlinear_term()` - Recursive amplification term
* `ego_symmetry_breaking()` - Ego formation through symmetry breaking
* `meditation_lambda_damping()` - Meditation as λ-damping

### `/archetypes`

* Planetary operator definitions
* Aspect tensor constructor

### `/topology` ✅

* `compute_persistence_diagram()` - Persistent homology computation
* `compute_betti_numbers()` - Topological feature counting
* `compute_joy_field()` - Joy as negative Ricci curvature
* `detect_topological_motifs()` - Archetypal pattern detection
* `classify_attractor_type()` - Fixed point, limit cycle, strange attractor

### `/symbols` ✅

* `generate_narrative()` - Symbolic interpretation of field topology
* `interpret_motifs()` - Archetypal pattern recognition
* `detect_threshold_crossings()` - Significant transition detection
* `create_event_log()` - Narrative event logging
* `NarrativeEvent` - Event representation class

### `/quantum`

* Hilbert space state constructor
* Entanglement entropy calculator
* Berry phase tracker

### `/tda`

* Persistent diagrams
* Betti analysis over archetypal time-series
* Topological alignment engine

### `/ml`

* Entanglement classifier
* Archetypal pattern recognizer
* Sequence predictor (LSTM / Transformer)

### `/frontend`

* React + Recharts + Shadcn
* AstroChart & ASTRA Field Viewer
* Entanglement graph and Betti overlay dashboards

### `/data`

* Ephemeris loaders (Swiss Ephemeris, JPL)
* Psychological survey data connectors
* Narrative extraction pipeline (NLP, archetype tagging)

### `/docs`

* `ASTRA_PRD_Full_Original.md` - Primary requirements document
* `QuantumAstrology_PRD.md`
* System diagrams, use cases, research references

## Testing Framework 🧪

ASTRA includes a comprehensive testing framework to ensure all components work correctly:

### Diagnostic Test

* `tests/test_diagnostic.py` - Tests all ASTRA components end-to-end
* Verifies imports, field creation, evolution, topology, and narrative generation
* Generates detailed visualizations in `output/diagnostic/`

### Component Tests

* `tests/test_core.py` - Tests QualiaField initialization and state management
* `tests/test_evolution.py` - Tests field evolution via fKPZχ equation
* `tests/test_topology.py` - Tests graph creation and topological analysis
* `tests/test_narrative.py` - Tests narrative event generation
* `tests/test_simple.py` - Simple diagnostic for core functionality

### Running Tests


```bash
# Run the diagnostic test (checks all components)
python tests/test_diagnostic.py

# Run a specific component test
python tests/test_core.py

# List available tests
python main.py --test
```

## Development Roadmap 🗺️

### v0.1 ✅


* ✅ Integration with Kerykeion for astrological calculations
* ✅ χ-Layer: Field evolution via fKPZχ equation
* ✅ 𝓈-Layer: Topological analysis (Betti numbers, Ricci curvature)
* ✅ 𝓂-Layer: Symbolic narrative generation

### v0.2 🔄


* 🔄 Cross-modal coupling between different qualia fields
* 🔄 Interactive visualization of field evolution
* 🔄 Retrocausal extension (fKPZχ-R)

### v1.0


* 🔮 Complete SOAPDREAM implementation
* 🔮 Comprehensive archetypal pattern library
* 🔮 Web interface for chart analysis and visualization

## License 📜
TBD — Likely MIT (open science alignment)

## Credits 🙏

Inspired by:
* Ancient astrologers 🕰️
* Quantum weirdos 🔮
* Recursive mystics 🌀
* The divine absurdity of trying to simulate your soul with math 🧮

ASTRA is for anyone debugging reality and mapping their inner resonance field. 

*iykyk* 😉✨
