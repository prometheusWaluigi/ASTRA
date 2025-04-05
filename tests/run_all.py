"""
ASTRA Master Test Runner

One script to rule them all, one script to find them,
One script to bring them all, and in the darkness bind them.

This script runs all the component tests for the ASTRA project and
generates a comprehensive test report.
"""

import os
import sys
import time
import subprocess
import importlib
from datetime import datetime

# Create output directories
os.makedirs("output/tests", exist_ok=True)

# Define colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Test modules to run
TEST_MODULES = [
    {"name": "Core Module", "script": "test_core.py"},
    {"name": "Evolution", "script": "test_evolution.py"},
    {"name": "Topology", "script": "test_topology.py"},
    {"name": "Narrative", "script": "test_narrative.py"}
]

def print_header(text):
    """Print a formatted header"""
    separator = "=" * 70
    print(f"\n{Colors.HEADER}{separator}")
    print(f"{text.center(70)}")
    print(f"{separator}{Colors.ENDC}\n")

def run_test(test_info):
    """Run a single test module"""
    name = test_info["name"]
    script = test_info["script"]
    
    print(f"{Colors.BLUE}Running {name} tests...{Colors.ENDC}")
    
    start_time = time.time()
    success = False
    output = ""
    
    try:
        # Run the test script as a subprocess
        result = subprocess.run(
            [sys.executable, os.path.join("tests", script)],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        output = result.stdout
        if result.stderr:
            output += f"\nSTDERR:\n{result.stderr}"
            
        success = result.returncode == 0
        
    except subprocess.TimeoutExpired:
        output = f"Test timed out after 5 minutes"
    except Exception as e:
        output = f"Error running test: {str(e)}"
    
    duration = time.time() - start_time
    
    # Print a brief summary
    status = f"{Colors.GREEN}PASSED" if success else f"{Colors.RED}FAILED"
    print(f"{status} in {duration:.2f} seconds{Colors.ENDC}")
    
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
    print_header("ASTRA MASTER TEST SUITE")
    print(f"Starting tests at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python version: {sys.version.split()[0]}")
    
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
    print(f"Passed: {Colors.GREEN}{passed_tests}{Colors.ENDC}")
    print(f"Failed: {Colors.RED if failed_tests > 0 else Colors.GREEN}{failed_tests}{Colors.ENDC}")
    print(f"Total duration: {total_duration:.2f} seconds")
    
    # Print detailed results
    print("\nDetailed results:")
    for i, result in enumerate(results, 1):
        status = f"{Colors.GREEN}PASSED" if result["success"] else f"{Colors.RED}FAILED"
        print(f"{i}. {result['name']} ({result['script']}): {status}{Colors.ENDC} in {result['duration']:.2f}s")
        print(f"   Log: {result['log_file']}")
    
    # Create a summary log
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
    
    # Final message with Lord of the Rings theme
    print_header("THE ONE RING")
    
    if failed_tests == 0:
        print(f"{Colors.GREEN}ALL TESTS PASSED!")
        print("\n\"It's done. It's over.\" - Frodo Baggins{Colors.ENDC}")
    else:
        print(f"{Colors.YELLOW}{failed_tests} TEST(S) FAILED")
        print("\n\"Even the smallest person can change the course of the future.\" - Galadriel{Colors.ENDC}")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    # Run from the project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    os.chdir(project_root)
    
    success = run_all_tests()
    sys.exit(0 if success else 1)
