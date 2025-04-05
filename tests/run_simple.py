"""
ASTRA Simple Test Runner

A robust test runner that works across all environments
by avoiding Unicode characters and fancy formatting.
"""

import os
import sys
import time
import subprocess
from datetime import datetime

# Create output directories
os.makedirs("output/tests", exist_ok=True)

# Test modules to run
TEST_MODULES = [
    {"name": "Core Module", "script": "test_core.py"},
    {"name": "Evolution", "script": "test_evolution.py"},
    {"name": "Topology", "script": "test_topology.py"},
    {"name": "Narrative", "script": "test_narrative.py"}
]

def print_separator(char="-", length=60):
    """Print a separator line"""
    print(char * length)

def print_header(title):
    """Print a formatted header"""
    print_separator("=")
    print(title.center(60))
    print_separator("=")
    print()

def run_test(test_info):
    """Run a single test module and handle output encoding issues"""
    name = test_info["name"]
    script = test_info["script"]
    
    print(f"Running {name} tests...")
    print_separator("-")
    
    start_time = time.time()
    success = False
    output = ""
    
    try:
        # Run the test script as a subprocess
        # Directly open process to handle output in real-time and avoid encoding issues
        process = subprocess.Popen(
            [sys.executable, os.path.join("tests", script)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            errors='replace'  # Handle encoding errors by replacing problematic characters
        )
        
        # Collect stdout and print in real-time
        stdout_lines = []
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            if line:
                # Replace potential problematic characters
                safe_line = line.strip()
                print(f"  {safe_line}")
                stdout_lines.append(safe_line)
        
        # Get return code and stderr
        rc = process.poll()
        stderr = process.stderr.read()
        
        # Print errors if any
        if stderr:
            print("\nErrors:")
            for line in stderr.splitlines():
                print(f"  {line}")
        
        # Determine success
        success = rc == 0
        
        # Combine output
        output = "\n".join(stdout_lines)
        if stderr:
            output += f"\n\nSTDERR:\n{stderr}"
            
    except Exception as e:
        output = f"Error running test: {str(e)}"
        print(output)
    
    duration = time.time() - start_time
    
    # Print a brief summary
    status = "PASSED" if success else "FAILED"
    print(f"\nResult: {status} in {duration:.2f} seconds")
    print_separator("-")
    
    # Save output to log file
    log_dir = os.path.join("output", "tests")
    log_file = os.path.join(log_dir, f"{os.path.splitext(script)[0]}_log.txt")
    
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"ASTRA TEST LOG: {name}\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Duration: {duration:.2f} seconds\n")
        f.write(f"Status: {'PASSED' if success else 'FAILED'}\n\n")
        f.write("OUTPUT:\n")
        f.write(output)
    
    return {
        "name": name,
        "script": script,
        "success": success,
        "duration": duration,
        "log_file": log_file
    }

def run_all_tests():
    """Run all test modules and collect results"""
    print_header("ASTRA SIMPLE TEST RUNNER")
    print(f"Starting tests at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python version: {sys.version.split()[0]}")
    print()
    
    results = []
    total_start_time = time.time()
    
    for test in TEST_MODULES:
        result = run_test(test)
        results.append(result)
    
    total_duration = time.time() - total_start_time
    
    # Generate summary
    print_header("TEST SUMMARY")
    
    total_tests = len(results)
    passed_tests = sum(1 for r in results if r["success"])
    failed_tests = total_tests - passed_tests
    
    print(f"Total tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    print(f"Total duration: {total_duration:.2f} seconds")
    
    # Print detailed results
    print("\nDetailed results:")
    for i, result in enumerate(results, 1):
        status = "PASSED" if result["success"] else "FAILED"
        print(f"{i}. {result['name']} ({result['script']}): {status} in {result['duration']:.2f}s")
        print(f"   Log: {result['log_file']}")
    
    # Create a summary log with timestamp
    summary_log = os.path.join("output", "tests", f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    with open(summary_log, "w", encoding="utf-8") as f:
        f.write(f"ASTRA TEST SUMMARY\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total duration: {total_duration:.2f} seconds\n\n")
        f.write(f"Total tests: {total_tests}\n")
        f.write(f"Passed: {passed_tests}\n")
        f.write(f"Failed: {failed_tests}\n\n")
        
        f.write("Detailed results:\n")
        for i, result in enumerate(results, 1):
            f.write(f"{i}. {result['name']} ({result['script']}): {'PASSED' if result['success'] else 'FAILED'} in {result['duration']:.2f}s\n")
            f.write(f"   Log: {result['log_file']}\n")
    
    print(f"\nFull summary saved to: {summary_log}")
    
    # Final message
    print_header("TEST COMPLETED")
    
    if failed_tests == 0:
        print("ALL TESTS PASSED!")
        print("\"It's done. It's over.\" - Frodo Baggins")
    else:
        print(f"{failed_tests} TEST(S) FAILED")
        print("\"Even the smallest person can change the course of the future.\" - Galadriel")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    # Run from the project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    os.chdir(project_root)
    
    success = run_all_tests()
    sys.exit(0 if success else 1)
