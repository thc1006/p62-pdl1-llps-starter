# Deployment Plan: Interactive LLPS Prediction Platform

## Objective
Create a **web-based** platform where researchers can:
1. Submit protein sequences
2. Get LLPS predictions from multiple tools
3. Visualize predictions on AlphaFold structures
4. Download results + mutation recommendations

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Web Interface (Streamlit)                 │
│  - Sequence input                                            │
│  - UniProt ID lookup                                         │
│  - Batch upload (CSV/FASTA)                                  │
└───────────────────┬─────────────────────────────────────────┘
                    │
                    ↓
┌─────────────────────────────────────────────────────────────┐
│               Backend (Flask/FastAPI)                        │
│  - API endpoints for predictions                             │
│  - Job queue (Celery/Redis)                                  │
│  - Result caching (MongoDB/PostgreSQL)                       │
└───────────┬────────────────┬────────────────┬───────────────┘
            │                │                │
            ↓                ↓                ↓
   ┌──────────────┐  ┌─────────────┐  ┌─────────────┐
   │  Phaseek GPU │  │  FuzDrop    │  │  Disorder   │
   │  (Local)     │  │  (API)      │  │  (Local)    │
   └──────────────┘  └─────────────┘  └─────────────┘
            │                │                │
            └────────────────┴────────────────┘
                           │
                           ↓
           ┌──────────────────────────────────┐
           │   Results Aggregation + Viz      │
           │   - Consensus score              │
           │   - 3D structure mapping         │
           │   - Mutation predictions         │
           └──────────────────────────────────┘
```

---

## Implementation Phases

### Phase 1: Core Prediction Engine (Week 1-2)

**Tasks:**
- [ ] Setup Docker container with GPU support
- [ ] Integrate Phaseek model (or fallback to local disorder prediction)
- [ ] Implement API wrappers for FuzDrop, PhaSePred
- [ ] Build consensus scoring algorithm

**Deliverables:**
- `scripts/llps_prediction_api.py` - Core prediction engine
- `docker-compose.yml` - GPU + web stack
- `tests/test_predictions.py` - Unit tests

---

### Phase 2: Web Interface (Week 3)

**Tasks:**
- [ ] Build Streamlit frontend
  - Sequence input form
  - UniProt ID autocomplete
  - Progress bar for long jobs
- [ ] Integrate with backend API
- [ ] Add result visualization
  - Disorder plot
  - LLPS score heatmap
  - 3D structure viewer (Mol* or PyMOL.js)

**Deliverables:**
- `app.py` - Streamlit app
- `templates/` - HTML templates
- `static/` - CSS/JS assets

---

### Phase 3: Advanced Features (Week 4)

**Tasks:**
- [ ] Batch prediction (upload CSV with 100+ proteins)
- [ ] Mutation effect calculator (FoldX integration)
- [ ] Export results (PDF report, CSV table, PDB with annotations)
- [ ] User accounts (save prediction history)

**Deliverables:**
- `scripts/batch_processor.py` - Parallel processing
- `scripts/mutation_scanner.py` - FoldX wrapper
- `reports/` - PDF generation templates

---

### Phase 4: Community Deployment (Week 5-6)

**Tasks:**
- [ ] Deploy to cloud (AWS/GCP with GPU instances)
- [ ] Setup CI/CD (GitHub Actions)
- [ ] Create documentation (user guide, API docs)
- [ ] Beta testing with 10 research groups

**Deliverables:**
- `deploy/` - Kubernetes manifests or Terraform configs
- `docs/` - Sphinx/MkDocs documentation
- `README.md` - Quick start guide

---

## Technology Stack

| Component | Technology | Justification |
|-----------|-----------|---------------|
| **Frontend** | Streamlit | Rapid prototyping, Python-native |
| **Backend** | FastAPI | Modern async API, auto-docs |
| **GPU Compute** | Docker + CUDA | Portable, reproducible |
| **Database** | PostgreSQL | Structured data + JSONB for flexibility |
| **Cache** | Redis | Fast lookup for repeated queries |
| **Queue** | Celery | Async job processing for long runs |
| **Visualization** | Plotly + Mol* | Interactive, publication-quality |
| **Deployment** | Kubernetes | Scalable, auto-healing |

---

## Hardware Requirements

### Minimum (Development):
- GPU: NVIDIA RTX 3050 (4GB VRAM) ✓ **We have this**
- RAM: 16GB
- Storage: 50GB SSD

### Production (Cloud):
- GPU: NVIDIA A100 (40GB) or T4 (16GB)
- RAM: 64GB
- Storage: 500GB SSD
- Bandwidth: 100 Mbps

### Estimated Cost:
- AWS g4dn.xlarge (T4 GPU): ~$0.526/hour = ~$380/month
- Free tier: Streamlit Community Cloud (CPU only, for demo)

---

## User Stories to Test

### Story 1: Researcher submits p62 sequence
**Steps:**
1. Visit platform: `https://llps-pdl1.bio`
2. Paste p62 PB1 sequence (103 aa)
3. Click "Predict"
4. Wait 30 seconds (GPU inference)
5. View results:
   - LLPS score: 0.72 (HIGH)
   - IDR regions: 15-45, 80-103
   - 3D structure: Hotspots highlighted
6. Download PDF report

**Expected:** Matches our offline predictions

---

### Story 2: Drug discovery team screens 1000 compounds
**Steps:**
1. Upload CSV: `compound_library.csv` (SMILES strings)
2. Select target: "p62 PB1 oligomerization interface"
3. Run virtual screening (docking + LLPS disruption score)
4. Download top 100 hits
5. Order compounds for in vitro testing

**Expected:** Identify condensate-disrupting molecules

---

## Success Metrics

### Technical:
- [ ] <1 min prediction time for single protein (GPU)
- [ ] 95%+ uptime (cloud deployment)
- [ ] Support 100 concurrent users

### Scientific:
- [ ] Validate 10 predictions experimentally
- [ ] Publish method paper (Bioinformatics or NAR Web Server Issue)
- [ ] 100+ users in first 6 months

### Community:
- [ ] GitHub stars: >500
- [ ] Citations: >10 in first year
- [ ] Integrate into CD-CODE database

---

## Open Source Release

**Repository:** `github.com/[your-org]/llps-pdl1-platform`

**License:** MIT (permissive for academic + commercial use)

**Components to release:**
1. Core prediction models
2. Web application (Streamlit + FastAPI)
3. Docker images (GPU + CPU versions)
4. Benchmark datasets
5. Tutorials + Jupyter notebooks

---

## Timeline Summary

| Week | Milestone |
|------|-----------|
| 1-2  | Core engine + API |
| 3    | Web interface (Streamlit) |
| 4    | Advanced features |
| 5    | Cloud deployment |
| 6    | Beta testing + docs |
| 7-8  | Public launch + paper submission |

**Total:** 8 weeks from start to publication-ready platform

---

## Next Immediate Actions (Today)

1. ✅ Run local LLPS predictions on p62/PD-L1
2. ✅ Generate user stories document
3. ⏳ Build minimal Streamlit prototype
4. ⏳ Test FuzDrop API integration
5. ⏳ Draft method paper outline

