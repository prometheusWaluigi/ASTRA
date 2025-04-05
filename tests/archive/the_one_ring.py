"""
The One Ring - Simple Master Test for ASTRA

One Test to rule them all, One Test to find them,
One Test to bring them all and in the darkness bind them.
"""

import os
import sys
import time
import subprocess
from datetime import datetime

# List of test scripts
TESTS = [
    "test_core.py",
    "test_enhanced.py", 
    "test_narrative_basic.py",
    "test_narrative_simple.py",
    "test_narrative.py",
    "test_topology_fixed.py"
]

def run_script(script_path):
    """Run a Python script and return success/failure"""
    print(f"\n>>> Running {script_path}...")
    start_time = time.time()
    
    try:
        # Run the script with a timeout
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=120  # 2 minute timeout
        )
        
        duration = time.time() - start_time
        
        # Check if successful
        if result.returncode == 0:
            print(f"✅ SUCCESS: {script_path} completed in {duration:.1f} seconds")
            return True
        else:
            print(f"❌ FAILED: {script_path} failed in {duration:.1f} seconds")
            print(f"Error: {result.stderr[:200]}...")
            return False
    
    except subprocess.TimeoutExpired:
        print(f"⏱️ TIMEOUT: {script_path} timed out after {time.time() - start_time:.1f} seconds")
        return False
    
    except Exception as e:
        print(f"⚠️ ERROR: Failed to run {script_path}: {str(e)}")
        return False

def main():
    """Run all tests and summarize results"""
    print("\n===== THE ONE RING - MASTER TEST FOR ASTRA =====")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Running {len(TESTS)} tests...")
    
    results = []
    
    # Run each test
    for test in TESTS:
        if os.path.exists(test):
            success = run_script(test)
            results.append((test, success))
        else:
            print(f"⚠️ WARNING: Test file {test} not found, skipping")
    
    # Print summary
    print("\n===== TEST SUMMARY =====")
    passed = sum(1 for _, success in results if success)
    failed = len(results) - passed
    
    print(f"Total tests: {len(results)}")
    print(f"Passed:      {passed}")
    print(f"Failed:      {failed}")
    
    # Show details of passed/failed tests
    if passed > 0:
        print("\nPassed tests:")
        for test, _ in filter(lambda x: x[1], results):
            print(f"  ✅ {test}")
    
    if failed > 0:
        print("\nFailed tests:")
        for test, _ in filter(lambda x: not x[1], results):
            print(f"  ❌ {test}")
    
    # Final message with Lord of the Rings theme
    print("\n" + "="*50)
    if failed == 0:
        print("ALL TESTS PASSED!")
        print("\"The road goes ever on and on, down from the door where it began.\"")
        print("- J.R.R. Tolkien")
    else:
        print(f"{failed} TESTS FAILED!")
        print("\"Not all those who wander are lost; the old that is strong does not wither.\"")
        print("- J.R.R. Tolkien")
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
