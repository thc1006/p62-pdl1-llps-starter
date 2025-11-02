#!/usr/bin/env python3
"""
Parallel Deconvolution Testing Framework
Tests multiple immune deconvolution approaches simultaneously
"""

import subprocess
import multiprocessing
import time
import json
import sys
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / "outputs" / "parallel_test_logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

def monitor_process(proc, log_file, timeout=600):
    """Monitor a process with timeout and stall detection"""
    start_time = time.time()
    last_size = 0
    stall_count = 0

    while proc.poll() is None:
        elapsed = time.time() - start_time

        # Check timeout
        if elapsed > timeout:
            proc.kill()
            return False, "TIMEOUT", elapsed

        # Check for stalled output
        try:
            current_size = log_file.stat().st_size
            if current_size == last_size:
                stall_count += 1
                if stall_count > 60:  # 60 seconds no output = stalled
                    proc.kill()
                    return False, "STALLED", elapsed
            else:
                stall_count = 0
                last_size = current_size
        except:
            pass

        time.sleep(1)

    elapsed = time.time() - start_time
    if proc.returncode == 0:
        return True, "SUCCESS", elapsed
    else:
        return False, f"EXIT_CODE_{proc.returncode}", elapsed

def test_approach(name, script_args, timeout=600):
    """Test a single deconvolution approach"""
    log_file = LOG_DIR / f"{name}.log"

    print(f"[START] {name}")
    print(f"  Command: {' '.join(script_args)}")
    print(f"  Log: {log_file}")

    start_time = time.time()

    try:
        with open(log_file, "w") as f:
            proc = subprocess.Popen(
                script_args,
                stdout=f,
                stderr=subprocess.STDOUT,
                cwd=BASE_DIR
            )

            success, reason, elapsed = monitor_process(proc, log_file, timeout)

            result = {
                "name": name,
                "success": success,
                "reason": reason,
                "elapsed": elapsed,
                "log_file": str(log_file),
                "timestamp": datetime.now().isoformat()
            }

            if success:
                print(f"[SUCCESS] {name} completed in {elapsed:.1f}s")
            else:
                print(f"[FAILED] {name} - {reason} after {elapsed:.1f}s")

            return result

    except Exception as e:
        elapsed = time.time() - start_time
        print(f"[ERROR] {name} - {str(e)}")
        return {
            "name": name,
            "success": False,
            "reason": f"EXCEPTION: {str(e)}",
            "elapsed": elapsed,
            "log_file": str(log_file),
            "timestamp": datetime.now().isoformat()
        }

def main():
    print("=" * 80)
    print("PARALLEL DECONVOLUTION TESTING FRAMEWORK")
    print("=" * 80)
    print()

    # Define test approaches
    approaches = [
        {
            "name": "timer2_prefiltered",
            "script": ["Rscript", "scripts/analysis/timer2_prefiltered.R"],
            "timeout": 600
        },
        {
            "name": "skip_2b_continue",
            "script": ["python", "scripts/analysis/skip_2b_continue.py"],
            "timeout": 300
        },
        {
            "name": "timer2_no_outlier_print",
            "script": ["Rscript", "scripts/analysis/timer2_no_print.R"],
            "timeout": 600
        },
        {
            "name": "use_xcell_method",
            "script": ["Rscript", "scripts/analysis/xcell_deconvolution.R"],
            "timeout": 600
        }
    ]

    print(f"Testing {len(approaches)} approaches in parallel...")
    print()

    # Run tests in parallel
    with multiprocessing.Pool(processes=len(approaches)) as pool:
        results = pool.starmap(
            test_approach,
            [(a["name"], a["script"], a["timeout"]) for a in approaches]
        )

    print()
    print("=" * 80)
    print("RESULTS SUMMARY")
    print("=" * 80)
    print()

    # Find winner
    winners = [r for r in results if r["success"]]

    if winners:
        winner = min(winners, key=lambda x: x["elapsed"])
        print(f"WINNER: {winner['name']}")
        print(f"  Completed in: {winner['elapsed']:.1f}s")
        print(f"  Log: {winner['log_file']}")
        print()
        print("Recommended action: Use this method for Phase 2B")
    else:
        print("NO SUCCESSFUL METHOD FOUND")
        print()
        print("All approaches failed:")
        for r in results:
            print(f"  - {r['name']}: {r['reason']}")
        print()
        print("Recommended action: Consider Docker containerization or alternative pipeline")

    # Save results
    results_file = LOG_DIR / f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_file, "w") as f:
        json.dump(results, f, indent=2)

    print()
    print(f"Full results saved to: {results_file}")

    return 0 if winners else 1

if __name__ == "__main__":
    sys.exit(main())
