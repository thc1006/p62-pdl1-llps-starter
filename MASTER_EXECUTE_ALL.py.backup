#!/usr/bin/env python3
"""
MASTER EXECUTION SCRIPT - Complete Research Pipeline
Orchestrates all phases from data download to final manuscript

Execution Order (Optimized):
Phase 1: Data Acquisition
Phase 2: Core Analysis with Real Data
Phase 3: Multi-Level Validation
Phase 4: Documentation & Figures
Phase 5: Final Publication Materials

Author: Automated Pipeline
Date: 2025-11-02
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

# =============================================================================
# Configuration
# =============================================================================

BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / "outputs" / "execution_logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Execution timestamp
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE = LOG_DIR / f"master_execution_{TIMESTAMP}.log"

# =============================================================================
# Phase Definitions (Optimized Sequence)
# =============================================================================

PHASES = [
    # Phase 1: Data Foundation
    {
        "phase": "1A",
        "name": "Setup Data Download Pipeline",
        "script": "scripts/data_pipeline/01_download_tcga_complete.py",
        "description": "Query GDC and setup download manifest",
        "critical": True,
        "estimated_time": "5 min",
        "prerequisites": []
    },
    {
        "phase": "1B",
        "name": "Download Complete TCGA Data",
        "script": None,  # Manual step
        "description": "Download RNA-seq + Clinical data (~50GB)",
        "critical": True,
        "estimated_time": "2-8 hours (depends on connection)",
        "prerequisites": ["1A"],
        "manual": True,
        "instructions": [
            "1. Use gdc-client or direct HTTP download",
            "2. Download TCGA-LUAD, TCGA-LUSC, TCGA-SKCM",
            "3. Verify file integrity"
        ]
    },
    {
        "phase": "1C",
        "name": "Process Expression Data",
        "script": "scripts/data_pipeline/02_process_expression.py",
        "description": "Normalize, QC, combine all projects",
        "critical": True,
        "estimated_time": "30-60 min",
        "prerequisites": ["1B"]
    },
    {
        "phase": "1D",
        "name": "Process Clinical Data",
        "script": "scripts/data_pipeline/03_process_clinical.py",
        "description": "Extract OS, stage, demographics",
        "critical": True,
        "estimated_time": "10 min",
        "prerequisites": ["1B"]
    },

    # Phase 2: Core Analysis (Fixed Methods)
    {
        "phase": "2A",
        "name": "Re-run Fixed Analysis with Real Data",
        "script": "scripts/excellence_upgrade/AUTOMATE_ALL_FIXES.py",
        "description": "Stratified Cox + Fixed Partial Correlation + CPTAC",
        "critical": True,
        "estimated_time": "5 min",
        "prerequisites": ["1C", "1D"]
    },
    {
        "phase": "2B",
        "name": "TIMER2.0 Immune Deconvolution",
        "script": "scripts/analysis/timer2_deconvolution.R",
        "description": "Calculate 6 immune cell type fractions",
        "critical": True,
        "estimated_time": "15 min",
        "prerequisites": ["1C"]
    },
    {
        "phase": "2C",
        "name": "Re-run Partial Correlation with TIMER2 Scores",
        "script": "scripts/excellence_upgrade/stage3_v3_timer2_confounders.py",
        "description": "Use real immune scores instead of fallback",
        "critical": True,
        "estimated_time": "3 min",
        "prerequisites": ["2A", "2B"]
    },

    # Phase 3: Multi-Level Validation
    {
        "phase": "3A",
        "name": "Single-Cell Validation (TISCH2)",
        "script": "scripts/analysis/single_cell_validation.py",
        "description": "Validate correlations in tumor vs immune cells",
        "critical": False,
        "estimated_time": "20 min",
        "prerequisites": ["2A"]
    },
    {
        "phase": "3B",
        "name": "External Cohort Validation (GEO)",
        "script": "scripts/analysis/external_validation_geo.py",
        "description": "Validate in 3+ independent cohorts",
        "critical": False,
        "estimated_time": "30 min",
        "prerequisites": ["2A"]
    },
    {
        "phase": "3C",
        "name": "Sensitivity Analysis",
        "script": "scripts/analysis/sensitivity_analysis.py",
        "description": "Per-cancer, outlier exclusion, bootstrap",
        "critical": False,
        "estimated_time": "10 min",
        "prerequisites": ["2C"]
    },

    # Phase 4: Visualization & Documentation
    {
        "phase": "4A",
        "name": "Generate Publication-Quality Figures",
        "script": "scripts/figures/generate_all_figures.py",
        "description": "All main + supplementary figures",
        "critical": True,
        "estimated_time": "15 min",
        "prerequisites": ["2C", "3A", "3B", "3C"]
    },
    {
        "phase": "4B",
        "name": "Update Manuscript",
        "script": "scripts/manuscript/update_manuscript.py",
        "description": "Update with real results, fix methods",
        "critical": True,
        "estimated_time": "5 min",
        "prerequisites": ["4A"]
    },

    # Phase 5: Final Materials
    {
        "phase": "5A",
        "name": "Generate Final PDF",
        "script": "scripts/manuscript/generate_pdf.py",
        "description": "Convert markdown to publication PDF",
        "critical": True,
        "estimated_time": "2 min",
        "prerequisites": ["4B"]
    },
    {
        "phase": "5B",
        "name": "Prepare Supplementary Materials",
        "script": "scripts/submission/prepare_supplementary.py",
        "description": "Tables, figures, code archive",
        "critical": True,
        "estimated_time": "5 min",
        "prerequisites": ["5A"]
    },
    {
        "phase": "5C",
        "name": "Generate Submission Package",
        "script": "scripts/submission/create_submission_package.py",
        "description": "Zip all materials for journal submission",
        "critical": True,
        "estimated_time": "2 min",
        "prerequisites": ["5B"]
    }
]

# =============================================================================
# Logging
# =============================================================================

def log(message: str, level: str = "INFO"):
    """Write log message"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] [{level}] {message}"

    print(log_msg)

    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_msg + "\n")

# =============================================================================
# Phase Execution
# =============================================================================

def check_prerequisites(phase: Dict, completed: List[str]) -> bool:
    """
    Check if all prerequisites are met

    Args:
        phase: Phase definition
        completed: List of completed phase IDs

    Returns:
        True if all prerequisites met
    """
    prereqs = phase.get("prerequisites", [])

    if not prereqs:
        return True

    for prereq in prereqs:
        if prereq not in completed:
            return False

    return True

def execute_phase(phase: Dict) -> Tuple[bool, float]:
    """
    Execute a single phase

    Args:
        phase: Phase definition

    Returns:
        (success, runtime_seconds)
    """
    import sys  # Import at function start to avoid scoping issues

    phase_id = phase["phase"]
    phase_name = phase["name"]

    log("="*80)
    log(f"PHASE {phase_id}: {phase_name}", "PHASE")
    log("="*80)
    log(f"Description: {phase['description']}")
    log(f"Estimated time: {phase['estimated_time']}")

    # Manual phase
    if phase.get("manual", False):
        log("This is a MANUAL phase", "WARN")
        log("Instructions:")
        for instruction in phase.get("instructions", []):
            log(f"  {instruction}")

        # Check for auto-yes flag
        auto_yes = '--auto-yes' in sys.argv or '-y' in sys.argv

        if auto_yes:
            log("\n[AUTO-YES] Skipping manual phase (will need to run separately)", "WARN")
            log("Manual phase auto-skipped", "SKIP")
            return False, 0.0
        else:
            response = input("\nHave you completed this step? (y/n): ").strip().lower()

            if response == 'y':
                log("Manual phase marked as complete", "OK")
                return True, 0.0
            else:
                log("Manual phase skipped/failed", "FAIL")
                return False, 0.0

    # Script phase
    script_path = BASE_DIR / phase["script"]

    if not script_path.exists():
        log(f"Script not found: {script_path}", "ERROR")
        log(f"Skipping phase {phase_id}", "WARN")
        return False, 0.0

    # Execute
    log(f"Executing: {script_path}")

    start_time = time.time()

    try:
        # Determine interpreter
        if script_path.suffix == '.py':
            cmd = [sys.executable, str(script_path)]
        elif script_path.suffix == '.R':
            cmd = ["Rscript", str(script_path)]
        elif script_path.suffix == '.sh':
            cmd = ["bash", str(script_path)]
        else:
            log(f"Unknown script type: {script_path.suffix}", "ERROR")
            return False, 0.0

        # Prepare environment with auto-download flag and UTF-8 encoding
        env = os.environ.copy()
        auto_yes = '--auto-yes' in sys.argv or '-y' in sys.argv
        if auto_yes:
            env['AUTO_DOWNLOAD'] = '1'
        env['PYTHONIOENCODING'] = 'utf-8'

        # Run
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=BASE_DIR,
            env=env,
            timeout=7200  # 2 hour timeout
        )

        runtime = time.time() - start_time

        # Log output
        if result.stdout:
            log("STDOUT:", "DEBUG")
            for line in result.stdout.split('\n')[:50]:  # First 50 lines
                log(f"  {line}", "DEBUG")

        if result.stderr:
            log("STDERR:", "DEBUG")
            for line in result.stderr.split('\n')[:50]:
                log(f"  {line}", "DEBUG")

        # Check success
        if result.returncode == 0:
            log(f"Phase {phase_id} completed successfully ({runtime:.1f}s)", "OK")
            return True, runtime
        else:
            log(f"Phase {phase_id} FAILED (exit code {result.returncode})", "FAIL")
            return False, runtime

    except subprocess.TimeoutExpired:
        runtime = time.time() - start_time
        log(f"Phase {phase_id} TIMEOUT after {runtime:.1f}s", "FAIL")
        return False, runtime

    except Exception as e:
        runtime = time.time() - start_time
        log(f"Phase {phase_id} ERROR: {e}", "FAIL")
        return False, runtime

# =============================================================================
# Main Execution
# =============================================================================

def main():
    """
    Main execution pipeline
    """
    import sys

    # Check for auto-yes flag
    auto_yes = '--auto-yes' in sys.argv or '-y' in sys.argv

    log("\n" + "="*80)
    log("MASTER EXECUTION PIPELINE - COMPLETE RESEARCH WORKFLOW")
    log("="*80)
    log(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"Log file: {LOG_FILE}")

    # Display phase overview
    log("\n" + "-"*80)
    log("PHASE OVERVIEW")
    log("-"*80)

    total_estimated_time = 0
    for phase in PHASES:
        phase_id = phase["phase"]
        phase_name = phase["name"]
        critical = "[CRITICAL]" if phase["critical"] else "[OPTIONAL]"
        est_time = phase["estimated_time"]
        manual = "[MANUAL]" if phase.get("manual", False) else ""

        log(f"  {phase_id}: {phase_name} {critical} {manual}")
        log(f"       Time: {est_time}")

    log("-"*80)

    # Ask for confirmation
    log("\nThis will execute the complete research pipeline.")
    log("Estimated total time: 4-10 hours (mostly data download)")
    log("")

    if auto_yes:
        log("[AUTO-YES] Proceeding automatically...")
        response = 'yes'
    else:
        response = input("Do you want to proceed? (yes/no): ").strip().lower()

    if response not in ['yes', 'y']:
        log("Execution cancelled by user")
        return

    # Execute phases
    completed_phases = []
    failed_phases = []
    skipped_phases = []

    total_runtime = 0.0
    pipeline_start = time.time()

    for phase in PHASES:
        phase_id = phase["phase"]

        # Check prerequisites
        if not check_prerequisites(phase, completed_phases):
            log(f"\nPhase {phase_id}: Prerequisites not met, SKIPPING", "SKIP")
            skipped_phases.append(phase_id)
            continue

        # Execute
        success, runtime = execute_phase(phase)
        total_runtime += runtime

        if success:
            completed_phases.append(phase_id)
        else:
            failed_phases.append(phase_id)

            # Stop if critical phase fails
            if phase["critical"]:
                log(f"\nCritical phase {phase_id} FAILED - STOPPING PIPELINE", "CRITICAL")
                break

    # Final summary
    pipeline_runtime = time.time() - pipeline_start

    log("\n" + "="*80)
    log("EXECUTION COMPLETE")
    log("="*80)
    log(f"Total runtime: {pipeline_runtime/60:.1f} minutes")
    log(f"Completed: {len(completed_phases)}/{len(PHASES)}")
    log(f"Failed: {len(failed_phases)}")
    log(f"Skipped: {len(skipped_phases)}")

    log("\nCompleted phases:")
    for phase_id in completed_phases:
        log(f"  [OK] {phase_id}")

    if failed_phases:
        log("\nFailed phases:")
        for phase_id in failed_phases:
            log(f"  [FAIL] {phase_id}")

    if skipped_phases:
        log("\nSkipped phases:")
        for phase_id in skipped_phases:
            log(f"  [SKIP] {phase_id}")

    # Save execution report
    report = {
        "timestamp": TIMESTAMP,
        "start_time": datetime.fromtimestamp(pipeline_start).isoformat(),
        "end_time": datetime.now().isoformat(),
        "total_runtime": pipeline_runtime,
        "completed": completed_phases,
        "failed": failed_phases,
        "skipped": skipped_phases,
        "success_rate": len(completed_phases) / len(PHASES) * 100
    }

    report_file = LOG_DIR / f"execution_report_{TIMESTAMP}.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)

    log(f"\n[SAVED] Execution report: {report_file}")
    log("="*80)

    # Success check
    if len(completed_phases) == len(PHASES):
        log("\nSUCCESS: All phases completed!", "SUCCESS")
        log("\nFinal outputs:")
        log("  - PDF: paper/manuscript_final.pdf")
        log("  - Figures: outputs/figures_publication/")
        log("  - Submission package: outputs/submission_package.zip")
        return 0
    else:
        log("\nPARTIAL SUCCESS: Some phases incomplete", "WARN")
        log("Review log file for details")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        log("\n\nExecution interrupted by user", "INTERRUPT")
        sys.exit(2)
    except Exception as e:
        log(f"\n\nUnexpected error: {e}", "CRITICAL")
        raise
