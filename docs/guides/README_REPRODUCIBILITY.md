# p62-PD-L1-LLPS: Reproducibility Guide
**Complete Workflow for Computational Analysis**

---

## Quick Start (5 Minutes)

```bash
# 1. Setup environment
pip install -r requirements.txt

# 2. Run literature gap analysis
python scripts/auto_literature_gap_analysis.py

# 3. Run LLPS predictions
python scripts/saprot_llps_prediction.py

# 4. Generate figures
python scripts/auto_generate_figures.py

# 5. View results
ls outputs/
```

**Output:**
- `outputs/literature_analysis/` - Gap analysis reports
- `outputs/llps_predictions/` - LLPS propensity scores
- `outputs/figures/` - Publication-quality figures (300 DPI)
- `outputs/tables/` - Summary tables (CSV)

---

## System Requirements

### Minimum
- **OS:** Windows 10/11 with WSL2, or Linux
- **RAM:** 16 GB
- **Storage:** 10 GB free
- **Python:** 3.8+

### Recommended (for GPU acceleration)
- **GPU:** NVIDIA GPU with ≥4 GB VRAM (e.g., RTX 3050)
- **CUDA:** 11.6+
- **Docker:** 28+ (for containerization)

---

## Installation

### Step 1: Clone Repository
```bash
git clone https://github.com/[your-org]/p62-pdl1-llps-starter
cd p62-pdl1-llps-starter
```

### Step 2: Install Dependencies
```bash
# Core Python packages
pip install pandas numpy scipy matplotlib seaborn

# For LLPS predictions
pip install torch transformers biopython

# For TCGA analysis
pip install requests lxml pyyaml

# Or install all at once
pip install -r requirements.txt
```

### Step 3: (Optional) Setup GPU Environment
```bash
# Check NVIDIA driver
nvidia-smi

# Install CUDA-enabled PyTorch
pip install torch==1.13.1+cu116 -f https://download.pytorch.org/whl/torch_stable.html
```

---

## Complete Workflow

### Phase 1: Literature Gap Analysis

**What it does:** Analyzes 178 papers from PubMed to identify research gaps.

```bash
python scripts/auto_literature_gap_analysis.py
```

**Expected output:**
- `outputs/literature_analysis/gap_analysis_report.md`
- `outputs/literature_analysis/gap_summary.json`

**Runtime:** ~2 minutes

**Key Finding:**
- HIGH priority gap: No papers on p62 condensates regulating PD-L1

---

### Phase 2: LLPS Propensity Predictions

**What it does:** Predicts LLPS propensity for p62, PD-L1, HIP1R, CMTM6, STUB1.

```bash
# Simple disorder-based prediction (fast, no GPU required)
python scripts/saprot_llps_prediction.py

# Advanced transformer model (requires GPU + model download ~2GB)
python scripts/saprot_real_inference.py
```

**Expected output:**
- `outputs/llps_predictions/saprot_llps_scores.json`
- `outputs/llps_predictions/saprot_real_predictions.json` (if using transformer)

**Runtime:**
- Simple: 1-2 minutes
- Transformer: 5-10 minutes (first run downloads model)

**Key Finding:**
- HIP1R shows highest LLPS propensity (0.475 - MEDIUM)
- Novel prediction not in literature

---

### Phase 3: TCGA Expression Correlation

**What it does:** Downloads and analyzes TCGA LUAD/LUSC expression data.

```bash
python scripts/gdc_expression_2025.py \
  --projects TCGA-LUAD TCGA-LUSC \
  --genes SQSTM1 CD274 HIP1R CMTM6 STUB1 \
  --max_samples 50 \
  --out outputs/gdc_expression
```

**Expected output:**
- `outputs/gdc_expression/*.tsv.gz` (raw files)
- `outputs/tcga_correlation/correlation_results.csv`

**Runtime:** ~10-20 minutes (depends on network speed)

**Key Finding:**
- SQSTM1-CD274 correlation: r=-0.073, P=0.617 (not significant)
- Supports context-dependent regulation hypothesis

---

### Phase 4: Generate Figures

**What it does:** Creates publication-quality figures (300 DPI PNG).

```bash
python scripts/auto_generate_figures.py
```

**Expected output:**
- `outputs/figures/Figure1_Literature_Gap.png` (timeline, rigor heatmap)
- `outputs/figures/Figure2_TCGA_Correlation.png` (scatter, heatmap)
- `outputs/figures/Figure3_Methodological_Framework.png` (workflow diagram)
- `outputs/tables/Table1_Summary.csv`

**Runtime:** ~1 minute

---

### Phase 5: Integrated Platform

**What it does:** Generates user stories and deployment plan.

```bash
python scripts/integrated_llps_platform.py
```

**Expected output:**
- `outputs/llps_integrated/user_stories.md` (5 testable hypotheses)
- `outputs/llps_integrated/deployment_plan.md` (8-week roadmap)

**Runtime:** <1 minute

---

## Troubleshooting

### Issue 1: TCGA Download Fails

**Symptom:** `ERROR: Not a gzipped file (b'# ')`

**Solution:** GDC files are plain TSV despite .gz extension. Fixed in latest script version using `compression='infer'`.

```bash
# If still failing, use quick analysis on existing files
python scripts/quick_partial_analysis.py
```

---

### Issue 2: GPU Out of Memory

**Symptom:** `RuntimeError: CUDA out of memory`

**Solution:** Use smaller model or CPU-only mode.

```bash
# Force CPU mode
export CUDA_VISIBLE_DEVICES=""
python scripts/saprot_llps_prediction.py
```

---

### Issue 3: Missing Dependencies

**Symptom:** `ModuleNotFoundError: No module named 'transformers'`

**Solution:** Install missing package.

```bash
pip install transformers
# or
pip install -r requirements.txt
```

---

## Validation

### Check Outputs

```bash
# Verify all outputs exist
ls outputs/literature_analysis/gap_analysis_report.md
ls outputs/llps_predictions/saprot_llps_scores.json
ls outputs/figures/*.png
ls outputs/tables/Table1_Summary.csv
```

### Reproduce Key Results

```bash
# Literature gap: Should find 178 papers
grep "Total Papers" outputs/literature_analysis/gap_analysis_report.md
# Expected: Total Papers Analyzed: 178

# LLPS prediction: HIP1R should be highest
cat outputs/llps_predictions/saprot_llps_scores.json | grep HIP1R
# Expected: "llps_score": 0.475
```

---

## Customization

### Analyze Different Genes

```python
# Edit scripts/gdc_expression_2025.py
parser.add_argument("--genes", nargs="+",
    default=["SQSTM1", "CD274", "YOUR_GENE_HERE"])
```

### Add New Proteins to LLPS Scan

```python
# Edit scripts/saprot_llps_prediction.py
sequences = {
    "your_protein": {
        "description": "Your protein description",
        "sequence": "MSKGEELFT..."  # Amino acid sequence
    }
}
```

### Modify Figure Styles

```python
# Edit scripts/auto_generate_figures.py
plt.rcParams['font.family'] = 'Arial'  # Change font
plt.rcParams['figure.dpi'] = 300       # Change resolution
```

---

## Performance Optimization

### Speed Up Literature Analysis

```bash
# Use smaller paper set for testing
# Edit evidence_dirs in auto_literature_gap_analysis.py
evidence_dirs = {
    "p62_pdl1_direct": "outputs/evidence/p62_pdl1_direct"  # Only one query
}
```

### Reduce TCGA Sample Size

```bash
python scripts/gdc_expression_2025.py --max_samples 20  # Faster download
```

### Use Pre-computed Results

```bash
# Skip re-running analysis, just regenerate figures
python scripts/auto_generate_figures.py
```

---

## Advanced Usage

### Docker Deployment

```bash
# Build GPU-enabled container
docker build -t p62-llps:latest -f Dockerfile .

# Run analysis in container
docker run --gpus all -v $(pwd):/workspace p62-llps:latest \
  python scripts/saprot_llps_prediction.py
```

### Batch Processing

```bash
# Run entire pipeline (all phases)
bash scripts/run_all.sh
```

**Create run_all.sh:**
```bash
#!/bin/bash
set -e

echo "[1/5] Literature gap analysis..."
python scripts/auto_literature_gap_analysis.py

echo "[2/5] LLPS predictions..."
python scripts/saprot_llps_prediction.py

echo "[3/5] TCGA analysis..."
python scripts/gdc_expression_2025.py --projects TCGA-LUAD TCGA-LUSC --max_samples 50

echo "[4/5] Generate figures..."
python scripts/auto_generate_figures.py

echo "[5/5] Integrated platform..."
python scripts/integrated_llps_platform.py

echo "Complete! Check outputs/ directory."
```

---

## Citations

If you use this workflow in your research, please cite:

```bibtex
@article{p62_pdl1_llps_2025,
  title={Context-dependent PD-L1 regulation by p62 condensates: Integrative computational framework},
  author={[Your Names]},
  journal={bioRxiv},
  year={2025},
  doi={10.1101/YYYY.MM.DD.XXXXXX}
}
```

**Key Tools Used:**
- SaProt: Structure-aware protein language model (ICLR 2024)
- GDC API: TCGA expression data (NIH/NCI)
- PubMed E-utilities: Literature mining (NCBI)

---

## Data Availability

**Raw data:**
- Literature evidence tables: `outputs/evidence/`
- TCGA expression files: `outputs/gdc_expression/`

**Processed data:**
- Summary tables: `outputs/tables/`
- LLPS predictions: `outputs/llps_predictions/`

**Figures:**
- Publication-ready: `outputs/figures/` (PNG, 300 DPI)

All data generated by this workflow are available in the `outputs/` directory.

---

## Limitations

1. **SaProt Model:** Requires 3D structure (via Foldseek) for full functionality. Sequence-only mode uses simplified disorder prediction.

2. **TCGA Sample Size:** Limited to 50 samples due to download time. Full cohort (~1000 samples) recommended for publication.

3. **Literature Analysis:** Auto-detection of LLPS methods incomplete. Manual curation recommended for final analysis.

4. **Computational Only:** No in vitro or cell-based validation performed.

---

## Support

**Issues:** Report bugs at https://github.com/[your-org]/p62-pdl1-llps-starter/issues

**Questions:** Contact [your email]

**Contributions:** Pull requests welcome!

---

## License

MIT License - See LICENSE file for details.

---

**Last Updated:** 2025-11-02
**Version:** 1.0
**Authors:** [Your Team]
