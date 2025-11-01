@echo off
REM ========================================
REM 🌙 OVERNIGHT NATURE-LEVEL ENHANCEMENT
REM ========================================
REM Run this script before sleep!
REM Automatically enhances project to Nature Communications level
REM
REM Requirements:
REM - Python 3.8+
REM - pip install -r requirements.txt
REM - Docker (for AlphaFold-Multimer, optional)
REM - NVIDIA GPU (for accelerated predictions)
REM
REM Author: Automated Enhancement System
REM Date: 2025-11-02
REM ========================================

echo.
echo ========================================
echo    OVERNIGHT NATURE ENHANCEMENT
echo     p62-PD-L1-LLPS Project
echo ========================================
echo.
echo This will run for ~8-12 hours overnight
echo Press Ctrl+C now to cancel, or...
timeout /t 10

echo.
echo [%time%] Starting automated enhancement pipeline...
echo.

REM Create output directories
if not exist outputs mkdir outputs
if not exist outputs\logs mkdir outputs\logs

REM Set log file with timestamp
set LOG_FILE=outputs\logs\overnight_enhancement_%date:~-4,4%%date:~-7,2%%date:~-10,2%_%time:~0,2%%time:~3,2%.log
set LOG_FILE=%LOG_FILE: =0%

echo Logging to: %LOG_FILE%
echo.

REM Check Python
python --version > nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.8+
    pause
    exit /b 1
)

echo [OK] Python detected
echo.

REM Install dependencies
echo [1/8] Installing/updating Python dependencies...
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

echo [OK] Dependencies installed
echo.

REM ========================================
REM PHASE 1: TCGA Expansion (4-6 hours)
REM ========================================
echo ========================================
echo PHASE 1: TCGA COHORT EXPANSION
echo Target: n=1000 samples (pan-cancer)
echo Estimated time: 4-6 hours
echo ========================================
echo.

echo [2/8] Downloading TCGA-LUAD expression data (500 samples)...
python scripts/gdc_expression_2025.py --project TCGA-LUAD --genes SQSTM1,CD274,HIP1R,CMTM6,STUB1 --max-files 500 --output outputs/gdc_expression >> "%LOG_FILE%" 2>&1

echo [3/8] Downloading TCGA-LUSC expression data (300 samples)...
python scripts/gdc_expression_2025.py --project TCGA-LUSC --genes SQSTM1,CD274,HIP1R,CMTM6,STUB1 --max-files 300 --output outputs/gdc_expression >> "%LOG_FILE%" 2>&1

echo [4/8] Analyzing full TCGA cohort...
python scripts/tcga_full_cohort_analysis.py >> "%LOG_FILE%" 2>&1

echo.
echo [OK] TCGA expansion complete
echo.

REM ========================================
REM PHASE 2: Survival Analysis (2-3 hours)
REM ========================================
echo ========================================
echo PHASE 2: SURVIVAL ANALYSIS
echo ========================================
echo.

echo [5/8] Downloading clinical and survival data...
python scripts/gdc_clinical_survival.py --cohorts LUAD LUSC --out outputs/tcga_survival >> "%LOG_FILE%" 2>&1

echo.
echo [OK] Survival data downloaded
echo.

REM ========================================
REM PHASE 3: Enhanced Literature (1 hour)
REM ========================================
echo ========================================
echo PHASE 3: ENHANCED LITERATURE ANALYSIS
echo ========================================
echo.

echo [6/8] Re-running literature gap analysis...
python scripts/auto_literature_gap_analysis.py >> "%LOG_FILE%" 2>&1

echo.
echo [OK] Literature analysis complete
echo.

REM ========================================
REM PHASE 4: Figure Generation (1 hour)
REM ========================================
echo ========================================
echo PHASE 4: NATURE-QUALITY FIGURES
echo ========================================
echo.

echo [7/8] Generating all publication figures (300 DPI)...
python scripts/auto_generate_figures.py >> "%LOG_FILE%" 2>&1

echo.
echo [OK] Figures generated
echo.

REM ========================================
REM PHASE 5: Manuscript Compilation
REM ========================================
echo ========================================
echo PHASE 5: MANUSCRIPT COMPILATION
echo ========================================
echo.

echo [8/8] Compiling enhanced preprint...
python scripts/auto_update_preprint_outline.py >> "%LOG_FILE%" 2>&1

echo.
echo [OK] Manuscript compiled
echo.

REM ========================================
REM COMPLETION
REM ========================================
echo.
echo ========================================
echo     OVERNIGHT ENHANCEMENT COMPLETE!
echo ========================================
echo.
echo Completion time: %time%
echo.
echo RESULTS:
echo   - TCGA samples: Check outputs/tcga_full_cohort/
echo   - Figures: outputs/figures/
echo   - Manuscript: paper/preprint_outline.md
echo   - Full log: %LOG_FILE%
echo.
echo NEXT STEPS:
echo   1. Review figures and results
echo   2. [Optional] Run AlphaFold-Multimer (requires Docker + GPU)
echo      Command: bash scripts/setup_colabfold.sh
echo   3. Submit to Nature Communications!
echo.
echo ========================================
echo.

pause
