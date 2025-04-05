"""
One Test to Rule Them All - ASTRA Master Test Script

This script sequentially runs all the ASTRA test modules to verify the entire system.
"""

import os
import sys
import time
import traceback
import subprocess
from datetime import datetime

# Create output directory
os.makedirs("output", exist_ok=True)

# Define test scripts to run
TEST_SCRIPTS = [
    "test_core.py",
    "test_enhanced.py",
    "test_narrative_basic.py",
    "test_narrative_simple.py",
    "test_narrative.py",
    "test_topology_fixed.py",
    "test_retrocausal.py"
]

# Print section heading
def print_header(text):
    print("\n" + "="*80)
    print(f" {text} ".center(80, "="))
    print("="*80 + "\n")

# Check if script exists
def script_exists(script):
    return os.path.exists(script)

# Main test function
def main():
    print_header("ASTRA MASTER TEST - ONE TEST TO RULE THEM ALL")
    print(f"Starting test run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python version: {sys.version.split()[0]}")
    print(f"Working directory: {os.getcwd()}")
    
    # Collect test results
    results = []
    
    # Run each test script
    for script in TEST_SCRIPTS:
        if not script_exists(script):
            print(f"- Script {script} not found, skipping...")
            continue
            
        print_header(f"RUNNING: {script}")
        
        start_time = time.time()
        try:
            # Run the script
            process = subprocess.Popen(
                [sys.executable, script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            # Print output in real-time
            print(f"[Output from {script}]")
            stdout_lines = []
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    line = output.strip()
                    print(f"  {line}")
                    stdout_lines.append(line)
            
            # Get return code and stderr
            return_code = process.poll()
            stderr = process.stderr.read()
            
            # Print any errors
            if stderr:
                print(f"\n[Errors from {script}]:")
                for line in stderr.strip().split('\n'):
                    print(f"  {line}")
            
            # Calculate duration and success
            duration = time.time() - start_time
            success = return_code == 0
            
            # Record result
            results.append({
                'script': script,
                'success': success,
                'duration': duration,
                'stdout_lines': len(stdout_lines),
                'stderr': stderr
            })
            
            # Print result
            status = "✅ PASSED" if success else "❌ FAILED"
            print(f"\n[Result: {status} in {duration:.2f} seconds]")
            
        except Exception as e:
            duration = time.time() - start_time
            print(f"\n[ERROR: Failed to run {script}]")
            traceback.print_exc()
            
            results.append({
                'script': script,
                'success': False,
                'duration': duration,
                'error': str(e)
            })
    
    # Print final summary
    print_header("TEST SUMMARY")
    
    total_tests = len(results)
    passed_tests = sum(1 for r in results if r['success'])
    failed_tests = total_tests - passed_tests
    total_time = sum(r['duration'] for r in results)
    
    print(f"Total tests run: {total_tests}")
    print(f"Tests passed:    {passed_tests}")
    print(f"Tests failed:    {failed_tests}")
    print(f"Total time:      {total_time:.2f} seconds")
    print("\nDetailed results:")
    
    for i, result in enumerate(results):
        status = "✅ PASSED" if result['success'] else "❌ FAILED"
        print(f"{i+1}. {result['script']}: {status} ({result['duration']:.2f} seconds)")
    
    # Print appropriate LOTR quote
    print_header("ONE TEST TO RULE THEM ALL")
    
    if failed_tests == 0:
        print('"It\'s the job that\'s never started as takes longest to finish." - Samwise Gamgee')
    else:
        print('"The way is shut. It was made by those who are Dead, and the Dead keep it." - Unknown')
    
    # Return exit code based on results
    return 0 if failed_tests == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
