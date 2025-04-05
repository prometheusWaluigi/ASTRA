"""
Master Test Script for ASTRA

This script runs all component tests for the ASTRA framework:
1. Core Field Implementation (test_core.py)
2. Enhanced fKPZχ Implementation (test_enhanced.py)
3. Basic Narrative Generation (test_narrative_basic.py)
4. Simplified Narrative Generation (test_narrative_simple.py)
5. Full Narrative Generation (test_narrative.py)
6. Fixed Topology Analysis (test_topology_fixed.py)
7. Retrocausal Extension (test_retrocausal.py)

One test to rule them all, one test to find them,
One test to bring them all and in the darkness bind them!
"""

import os
import sys
import time
import subprocess
import datetime
import traceback
from typing import List, Dict, Any, Tuple

# Create output directory if it doesn't exist
os.makedirs("output", exist_ok=True)
os.makedirs(os.path.join("output", "test_all"), exist_ok=True)

# Banner text for output formatting
def print_banner(text: str, width: int = 80) -> None:
    """Print a banner with the given text."""
    print("\n" + "=" * width)
    print(f"{text.center(width)}")
    print("=" * width + "\n")

# Run a test script and capture its output
def run_test(script_name: str) -> Tuple[bool, str, float]:
    """
    Run a test script and capture its output.
    
    Args:
        script_name: Name of the test script to run
        
    Returns:
        Tuple of (success, output, duration)
    """
    print(f"Running {script_name}...")
    start_time = time.time()
    
    try:
        print(f"  Executing: {sys.executable} {script_name}")
        # Run the script and capture output
        result = subprocess.run(
            [sys.executable, script_name], 
            capture_output=True, 
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        duration = time.time() - start_time
        success = result.returncode == 0
        output = result.stdout
        
        # Print a short preview of output
        output_preview = output.strip()
        if len(output_preview) > 300:
            output_preview = output_preview[:297] + "..."
        # Use a raw string to handle newlines properly
        print(f"  Output preview: ")
        for line in output_preview.split('\n')[:10]:  # Show only first 10 lines
            print(f"    {line}")
        if len(output_preview.split('\n')) > 10:
            print("    ...")
        
        if not success:
            error_info = f"\nError (return code {result.returncode}):\n{result.stderr}"
            output += error_info
            print(f"  Error details: {result.stderr[:200]}{'...' if len(result.stderr) > 200 else ''}")
        
        # Save output to a file
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = os.path.join("output", "test_all")
        output_file = os.path.join(output_dir, f"{os.path.splitext(script_name)[0]}_{timestamp}.log")
        
        with open(output_file, "w") as f:
            f.write(output)
        print(f"  Full log saved to: {output_file}")
        
        # Print summary
        status = "✓ PASSED" if success else "✗ FAILED"
        print(f"{status} in {duration:.2f} seconds")
        
        return success, output, duration
        
    except subprocess.TimeoutExpired:
        duration = time.time() - start_time
        output = f"Test timed out after {duration:.2f} seconds"
        print(f"✗ TIMED OUT in {duration:.2f} seconds")
        return False, output, duration
        
    except Exception as e:
        duration = time.time() - start_time
        output = f"Error running test: {str(e)}\n{traceback.format_exc()}"
        print(f"✗ ERROR in {duration:.2f} seconds: {str(e)}")
        return False, output, duration

# Tests to run
tests = [
    {"name": "Core Field Implementation", "script": "test_core.py"},
    {"name": "Enhanced fKPZχ Implementation", "script": "test_enhanced.py"},
    {"name": "Basic Narrative Generation", "script": "test_narrative_basic.py"},
    {"name": "Simplified Narrative Generation", "script": "test_narrative_simple.py"},
    {"name": "Full Narrative Generation", "script": "test_narrative.py"},
    {"name": "Fixed Topology Analysis", "script": "test_topology_fixed.py"}
]

# Add retrocausal test if it exists
if os.path.exists("test_retrocausal.py"):
    tests.append({"name": "Retrocausal Extension", "script": "test_retrocausal.py"})

# Print header
print_banner("ASTRA MASTER TEST SUITE")
print(f"Running {len(tests)} tests at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Python version: {sys.version}")
print(f"Output directory: {os.path.abspath(os.path.join('output', 'test_all'))}")

# Run all tests
results = []
all_passed = True
total_start_time = time.time()

for i, test in enumerate(tests):
    print_banner(f"Test {i+1}/{len(tests)}: {test['name']}")
    success, output, duration = run_test(test["script"])
    
    result = {
        "name": test["name"],
        "script": test["script"],
        "success": success,
        "duration": duration,
        "output": output
    }
    
    results.append(result)
    all_passed = all_passed and success

total_duration = time.time() - total_start_time

# Print summary
print_banner("TEST SUMMARY")
passed_count = sum(1 for r in results if r["success"])
print(f"Total: {len(results)} tests")
print(f"Passed: {passed_count} tests")
print(f"Failed: {len(results) - passed_count} tests")
print(f"Total duration: {total_duration:.2f} seconds")
print("\nDetailed Results:")

for i, result in enumerate(results):
    status = "✓ PASSED" if result["success"] else "✗ FAILED"
    print(f"{i+1}. {result['name']} ({result['script']}): {status} in {result['duration']:.2f} seconds")

# Print final status
if all_passed:
    print_banner("ALL TESTS PASSED!")
    print("The ASTRA framework is functioning correctly!\n")
else:
    print_banner("SOME TESTS FAILED")
    print("Please check the logs in the output directory for details.\n")

# Print appropriate Lord of the Rings quote based on result
if all_passed:
    print('"It\'s the job that\'s never started as takes longest to finish." - Samwise Gamgee')
else:
    print('"The way is shut. It was made by those who are Dead, and the Dead keep it." - Unknown')
