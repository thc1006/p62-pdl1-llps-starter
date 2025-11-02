#!/usr/bin/env python3
"""
AUTOMATED EXCELLENCE UPGRADE - All Fixes

"""
import subprocess
import sys
from pathlib import Path
import time
from datetime import datetime
import json

print("="*80)
print(" AUTOMATED EXCELLENCE UPGRADE - COMPLETE FIX")
print("="*80)
print(f"\nStarted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("\n[OK] THIS WILL FIX:")
print("  1. Circular adjustment in IFN-/immune scores")
print("  2. Cross-cancer Cox analysis issues")
print("  3. Missing Schoenfeld residuals test")
print("  4. Missing robustness checks (Spearman, bootstrap)")
print("  5. Missing VIF multicollinearity check")
print("="*80)

# ============================================================================
# Configuration
# ============================================================================
SCRIPTS_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPTS_DIR.parent.parent

stages = [
    {
        'name': 'Stage 2 v2: Fixed Stratified Cox Analysis',
        'script': 'stage2_v2_stratified_cox.py',
        'description': 'Fixes cross-cancer Cox + adds Schoenfeld test + VIF check',
        'critical': True
    },
    {
        'name': 'Stage 3 v2: Fixed Partial Correlation',
        'script': 'stage3_v2_fixed_partial_correlation.py',
        'description': 'Fixes circular adjustment + adds true IFN- signature',
        'critical': True
    },
    {
        'name': 'Stage 4: CPTAC Validation (rerun)',
        'script': 'stage4_cptac_validation.py',
        'description': 'Protein-level validation (no changes needed)',
        'critical': False
    }
]

# ============================================================================
# Execution
# ============================================================================
results = []

for i, stage in enumerate(stages, 1):
    print(f"\n{'='*80}")
    print(f"[STAGE {i}/{len(stages)}] {stage['name']}")
    print(f"{'='*80}")
    print(f"Script: {stage['script']}")
    print(f"Description: {stage['description']}")
    print(f"Critical: {'YES' if stage['critical'] else 'NO'}")

    script_path = SCRIPTS_DIR / stage['script']

    if not script_path.exists():
        print(f"\n[WARN] WARNING: Script not found: {script_path}")
        if stage['critical']:
            print("  This is a CRITICAL stage - cannot proceed!")
            results.append({
                'stage': stage['name'],
                'status': 'FAILED',
                'reason': 'Script not found',
                'runtime': 0
            })
            continue
        else:
            print("  Skipping non-critical stage...")
            results.append({
                'stage': stage['name'],
                'status': 'SKIPPED',
                'reason': 'Script not found',
                'runtime': 0
            })
            continue

    # Execute stage
    print(f"\n[RUN] Executing: python {script_path.name}")
    print("-" * 80)

    start_time = time.time()

    try:
        # Run script
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=600  # 10 minutes timeout per stage
        )

        runtime = time.time() - start_time

        # Print output
        if result.stdout:
            print(result.stdout)

        if result.stderr:
            print("STDERR:", result.stderr, file=sys.stderr)

        # Check success
        if result.returncode == 0:
            print(f"\n[OK] SUCCESS: {stage['name']} completed in {runtime:.1f}s")
            results.append({
                'stage': stage['name'],
                'status': 'SUCCESS',
                'runtime': runtime
            })
        else:
            print(f"\n[FAIL] FAILED: {stage['name']} (exit code {result.returncode})")
            results.append({
                'stage': stage['name'],
                'status': 'FAILED',
                'reason': f'Exit code {result.returncode}',
                'runtime': runtime
            })

            if stage['critical']:
                print("\n CRITICAL STAGE FAILED - STOPPING EXECUTION")
                break

    except subprocess.TimeoutExpired:
        runtime = time.time() - start_time
        print(f"\n[TIME] TIMEOUT: {stage['name']} exceeded 10 minutes")
        results.append({
            'stage': stage['name'],
            'status': 'TIMEOUT',
            'runtime': runtime
        })

        if stage['critical']:
            print("\n CRITICAL STAGE TIMEOUT - STOPPING EXECUTION")
            break

    except Exception as e:
        runtime = time.time() - start_time
        print(f"\n ERROR: {stage['name']} failed with exception:")
        print(f"  {type(e).__name__}: {e}")
        results.append({
            'stage': stage['name'],
            'status': 'ERROR',
            'reason': str(e),
            'runtime': runtime
        })

        if stage['critical']:
            print("\n CRITICAL STAGE ERROR - STOPPING EXECUTION")
            break

# ============================================================================
# Summary
# ============================================================================
print("\n" + "="*80)
print(" EXECUTION SUMMARY")
print("="*80)

total_runtime = sum(r.get('runtime', 0) for r in results)
success_count = sum(1 for r in results if r['status'] == 'SUCCESS')
failed_count = sum(1 for r in results if r['status'] in ['FAILED', 'ERROR', 'TIMEOUT'])

print(f"\nTotal stages: {len(results)}")
print(f"  [OK] Successful: {success_count}")
print(f"  [FAIL] Failed: {failed_count}")
print(f"  [TIME] Total runtime: {total_runtime:.1f}s ({total_runtime/60:.1f} minutes)")

print("\nDetailed Results:")
for r in results:
    status_icon = {
        'SUCCESS': '[OK]',
        'FAILED': '[FAIL]',
        'ERROR': '',
        'TIMEOUT': '[TIME]',
        'SKIPPED': '[SKIP]'
    }.get(r['status'], '[UNKNOWN]')

    print(f"  {status_icon} {r['stage']}: {r['status']} ({r.get('runtime', 0):.1f}s)")
    if 'reason' in r:
        print(f"     Reason: {r['reason']}")

# Save results
output_dir = Path("outputs/excellence_upgrade_results")
output_dir.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
results_file = output_dir / f"execution_results_{timestamp}.json"

with open(results_file, 'w') as f:
    json.dump({
        'timestamp': datetime.now().isoformat(),
        'total_runtime': total_runtime,
        'success_count': success_count,
        'failed_count': failed_count,
        'results': results
    }, f, indent=2)

print(f"\n[SAVED] {results_file}")

# Final verdict
print("\n" + "="*80)
if all(r['status'] == 'SUCCESS' for r in results if r.get('status')):
    print(" ALL FIXES COMPLETED SUCCESSFULLY!")
    print("="*80)
    print("\n[OK] WHAT WAS FIXED:")
    print("  1. [OK] Removed CD274-based IFN- proxy (no more circular adjustment)")
    print("  2. [OK] Used 18-gene T-cell inflamed GEP (Ayers 2017)")
    print("  3. [OK] Implemented stratified Cox by cancer type")
    print("  4. [OK] Added Schoenfeld residuals test")
    print("  5. [OK] Added VIF multicollinearity check")
    print("  6. [OK] Added Spearman correlation robustness")
    print("  7. [OK] Added bootstrap confidence intervals")
    print("\n NEXT STEPS:")
    print("  1. Review outputs in:")
    print("     - outputs/survival_analysis_v2_fixed/")
    print("     - outputs/partial_correlation_v2_fixed/")
    print("  2. Update manuscript Methods and Results sections")
    print("  3. Update README with fixed methodology")
    print("  4. Ready to submit to IF~10 journal!")
else:
    print("[WARN] SOME STAGES FAILED")
    print("="*80)
    print("\nPlease review error messages above and:")
    print("  1. Check if required data files exist")
    print("  2. Ensure all Python dependencies installed")
    print("  3. Run individual stages manually for debugging")

print(f"\nFinished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)
