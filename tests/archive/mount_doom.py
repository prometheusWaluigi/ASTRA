"""
Mount Doom - Final Test Script for ASTRA

This script runs all ASTRA components with ASCII-only output
to ensure compatibility with all terminals.
"""

import os
import sys
import time
import subprocess
from datetime import datetime

# Create output directory
os.makedirs("output", exist_ok=True)

# List of test scripts with ASCII-friendly names
TESTS = [
    {
        "name": "Core Field Implementation",
        "script": "test_core.py"
    },
    {
        "name": "Enhanced Evolution",
        "script": "test_enhanced.py"
    },
    {
        "name": "Basic Narrative Generation",
        "script": "test_narrative_basic.py"
    },
    {
        "name": "Simple Narrative Generation",
        "script": "test_narrative_simple.py"
    },
    {
        "name": "Full Narrative Generation",
        "script": "test_narrative.py"
    },
    {
        "name": "Fixed Topology Analysis",
        "script": "test_topology_fixed.py"
    }
]

def print_separator(char="-", length=60):
    """Print a separator line"""
    print(char * length)

def run_test(name, script_path):
    """Run a test script and return result details"""
    print(f"\nRunning: {name} ({script_path})")
    print_separator()
    
    start_time = time.time()
    success = False
    output = ""
    error = ""
    
    try:
        # Execute process and redirect output
        process = subprocess.run(
            [sys.executable, "-u", script_path],  # -u for unbuffered output
            capture_output=True,
            text=True,
            timeout=180  # 3 minute timeout
        )
        
        output = process.stdout
        error = process.stderr
        success = process.returncode == 0
        
        # Print abbreviated output (first 10 lines)
        print("First few lines of output:")
        for line in output.splitlines()[:10]:
            print(f"  {line}")
        
        if len(output.splitlines()) > 10:
            print("  ...")
            
        # Print abbreviated error if present
        if error:
            print("\nError encountered:")
            for line in error.splitlines()[:5]:
                print(f"  {line}")
            if len(error.splitlines()) > 5:
                print("  ...")
    
    except subprocess.TimeoutExpired:
        error = "Test timed out"
        print("ERROR: Test timed out after 3 minutes")
    
    except Exception as e:
        error = str(e)
        print(f"ERROR: {error}")
    
    # Calculate duration
    duration = time.time() - start_time
    
    # Print result
    result_status = "PASSED" if success else "FAILED"
    print(f"\nResult: {result_status} in {duration:.2f} seconds")
    print_separator()
    
    return {
        "name": name,
        "script": script_path,
        "success": success,
        "duration": duration,
        "output_length": len(output),
        "error_length": len(error)
    }

def main():
    """Run all tests and summarize results"""
    print("===== ASTRA FINAL TEST (MOUNT DOOM) =====")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python Version: {sys.version.split()[0]}")
    print(f"Working Directory: {os.getcwd()}")
    print(f"Total Tests: {len(TESTS)}")
    print_separator("=")
    
    results = []
    start_time = time.time()
    
    # Run each test
    for test in TESTS:
        name = test["name"]
        script = test["script"]
        
        if os.path.exists(script):
            result = run_test(name, script)
            results.append(result)
        else:
            print(f"\nWARNING: Test script {script} not found, skipping")
            results.append({
                "name": name,
                "script": script,
                "success": False,
                "duration": 0,
                "output_length": 0,
                "error_length": 0,
                "missing": True
            })
    
    # Calculate totals
    total_time = time.time() - start_time
    total_tests = len(results)
    passed_tests = sum(1 for r in results if r.get("success", False))
    failed_tests = total_tests - passed_tests
    
    # Print summary
    print("\n===== TEST SUMMARY =====")
    print(f"Total Tests:   {total_tests}")
    print(f"Passed Tests:  {passed_tests}")
    print(f"Failed Tests:  {failed_tests}")
    print(f"Total Time:    {total_time:.2f} seconds")
    print_separator()
    
    # Print detailed results
    print("\nDetailed Results:")
    for i, result in enumerate(results):
        status = "PASSED" if result.get("success", False) else "FAILED"
        if result.get("missing", False):
            status = "MISSING"
            
        print(f"{i+1}. {result['name']} ({result['script']}): {status} in {result['duration']:.2f}s")
    
    # Final message
    print_separator("=")
    if failed_tests == 0:
        print("SUCCESS: All tests passed!")
        print("\"It's done. It's over.\" - Frodo Baggins")
    else:
        print(f"ATTENTION: {failed_tests} test(s) failed.")
        print("\"The ring was trying to get back to its master.\" - Gandalf")
    
    return 0 if failed_tests == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
