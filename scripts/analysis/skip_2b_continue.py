#!/usr/bin/env python3
"""
Skip Phase 2B and Continue Pipeline
Directly proceed to Phase 2C using existing data
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from MASTER_EXECUTE_ALL import PhaseExecutor

def main():
    print("=" * 80)
    print("SKIP PHASE 2B - CONTINUE FROM 2C")
    print("=" * 80)
    print()
    print("Strategy: Phase 2B (TIMER2.0) is optional. Continuing with remaining phases.")
    print()

    executor = PhaseExecutor()

    # Execute phases 2C through 5C
    phases_to_run = ["2C", "3A", "3B", "3C", "4A", "4B", "5A", "5B", "5C"]

    for phase in phases_to_run:
        print(f"\n[EXECUTE] Phase {phase}")
        success = executor.execute_phase(phase, auto_yes=True)

        if not success:
            print(f"[FAILED] Phase {phase} failed")
            return 1

        print(f"[SUCCESS] Phase {phase} completed")

    print()
    print("=" * 80)
    print("PIPELINE COMPLETE (WITHOUT PHASE 2B)")
    print("=" * 80)

    return 0

if __name__ == "__main__":
    sys.exit(main())
