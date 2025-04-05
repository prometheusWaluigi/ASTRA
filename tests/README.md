# ASTRA Test Suite

This directory contains a comprehensive test suite for the ASTRA project, organized by module.

## Test Structure

- `test_core.py` - Tests the core QualiaField implementation
- `test_evolution.py` - Tests the field evolution dynamics
- `test_topology.py` - Tests the topology analysis features
- `test_narrative.py` - Tests the symbolic narrative generation
- `run_all.py` - Master script that runs all tests and generates a summary

## Running Tests

You can run individual tests:

```bash
python tests/test_core.py
python tests/test_evolution.py
python tests/test_topology.py
python tests/test_narrative.py
```

Or run all tests at once:

```bash
python tests/run_all.py
```

## Test Output

All test outputs are saved to the `output/tests/` directory:
- Visualizations
- Log files
- Summary reports

## Archive

The `archive/` directory contains older test scripts that have been superseded by the new test organization.
