# 🚀 US Server Quick Start

## One-Page Instructions for US Server Deployment

---

## Step 1: Clone Repository

```bash
cd /your/workspace/
git clone https://github.com/thc1006/p62-pdl1-llps-starter.git
cd p62-pdl1-llps-starter
```

---

## Step 2: Run Deployment Script

```bash
# One command to install everything
bash deploy_us_server.sh

# This will:
# ✅ Install Python 3.11+ dependencies
# ✅ Install R 4.3+ packages
# ✅ Install gdc-client
# ✅ Verify all requirements
```

---

## Step 3: Execute Pipeline

```bash
# After deploy_us_server.sh completes:
python MASTER_EXECUTE_ALL.py --auto-yes 2>&1 | tee execution.log

# OR if already in virtualenv:
source venv/bin/activate
python MASTER_EXECUTE_ALL.py --auto-yes
```

---

## Step 4: Monitor Progress (In Another Terminal)

```bash
# Watch execution log
tail -f outputs/execution_logs/master_execution_*.log

# Or more detailed:
watch -n 30 'tail -50 outputs/execution_logs/master_execution_*.log'
```

---

## Expected Timeline (US Server)

```
Phase 1A: Query GDC              ~5 min     ✓
Phase 1B: Download 6.5GB         ~30-45 min ✓ (Fast in US!)
Phase 1C: Process expression     ~35 min    ✓
Phase 1D: Process clinical       ~10 min    ✓
Phase 2A: Cox analysis           ~5 min     ✓
Phase 2B: TIMER2.0               ~15 min    ✓
Phase 2C: Partial correlation    ~3 min     ✓
Phase 3A-C: Validation           ~60 min    ✓
Phase 4A-B: Figures + manuscript ~20 min    ✓
Phase 5A-C: Submission package   ~9 min     ✓

TOTAL: ~3-4 hours (with US download speed)
```

---

## Verify Success

```bash
# Check execution report
cat outputs/execution_logs/execution_report_*.json | jq '.success_rate'
# Should show: 100.0

# Check outputs exist
ls -lh outputs/submission_package/*.zip
ls -lh outputs/figures_publication/Figure*.png
```

---

## Final Outputs

```
outputs/submission_package/PD-L1_Regulatory_Network_Submission_*.zip
├── 1_manuscript/manuscript_final.pdf  ← SUBMIT THIS
├── 2_main_figures/Figure1-4.png      ← 300 DPI
├── 3_supplementary_materials/
├── 4_cover_letter/
└── 5_code/
```

---

## Troubleshooting

### If gdc-client not found:
```bash
wget https://gdc.cancer.gov/files/public/file/gdc-client_v1.6.1_Ubuntu_x64.zip
unzip gdc-client_v1.6.1_Ubuntu_x64.zip
chmod +x gdc-client
sudo mv gdc-client /usr/local/bin/
```

### If Unicode errors:
```bash
export LC_ALL=en_US.UTF-8
export PYTHONIOENCODING=utf-8
python MASTER_EXECUTE_ALL.py --auto-yes
```

---

## For More Details

- **Complete Guide**: `HANDOFF_TO_US_SERVER.md` (48 pages)
- **Quick Reference**: `QUICK_START.md`
- **Pipeline Details**: `PIPELINE_EXECUTION_GUIDE.md`

---

## Questions for New Claude Session on US Server

**"Please help me execute the PD-L1 research pipeline that was handed off from Taiwan desktop. Review HANDOFF_TO_US_SERVER.md and execute python MASTER_EXECUTE_ALL.py --auto-yes. Monitor for errors and verify all 15 phases complete successfully."**

---

**That's it!** 🎉

Single command deployment, then automatic execution for 3-4 hours.

---

**Last Updated**: 2025-11-02
**Repo**: https://github.com/thc1006/p62-pdl1-llps-starter
