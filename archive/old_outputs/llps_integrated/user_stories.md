# User Stories for p62-PD-L1 LLPS Hypothesis Testing

## Story 1: "Does p62 PB1 domain form condensates with PD-L1?"

**As a:** Biochemist studying LLPS
**I want to:** Test if p62 and PD-L1 co-condense in vitro
**So that:** I can validate computational predictions

**Acceptance Criteria:**
- [ ] Purify recombinant p62-PB1 domain (aa 1-103)
- [ ] Purify PD-L1 cytoplasmic tail (aa 239-290)
- [ ] Mix at 1:1 molar ratio in PBS (150 mM NaCl)
- [ ] Measure turbidity at OD600 vs concentration (0.1-50 μM)
- [ ] Observe droplets by DIC microscopy
- [ ] Calculate Csat for p62 alone vs p62+PD-L1
- [ ] Expected: Csat shifts if co-condensation occurs

**Predicted Outcome (from our analysis):**
- p62 PB1: HIGH LLPS propensity (score >0.6)
- PD-L1 tail: MODERATE LLPS propensity (score ~0.5)
- Hypothesis: p62 recruits PD-L1 into condensates

**Validation Tools:**
1. FuzDrop visualization: Map predicted regions
2. Disorder prediction: Identify flexible linkers
3. AlphaFold structure: Guide domain boundaries

---

## Story 2: "Does autophagy flux blockade stabilize PD-L1?"

**As a:** Cancer biologist testing immunotherapy resistance
**I want to:** Measure PD-L1 half-life under autophagy stress
**So that:** I can test context-dependent regulation hypothesis

**Acceptance Criteria:**
- [ ] Treat cells with Bafilomycin A1 (100 nM, block autophagy flux)
- [ ] Measure PD-L1 half-life by cycloheximide chase (0, 2, 4, 8, 12h)
- [ ] Compare WT vs p62-KO cells
- [ ] Quantify surface PD-L1 by flow cytometry
- [ ] Expected: PD-L1 stabilized in WT + Baf A1, but not in p62-KO

**Predicted Outcome (from TCGA analysis):**
- Baseline: p62 promotes degradation (r=-0.073, null but negative trend)
- Flux blockade: p62 bodies sequester PD-L1 → protection
- p62-KO: No protection phenotype

**Validation Tools:**
1. TCGA stratification: Test in ATG5/7-low tumors
2. Immunofluorescence: p62 bodies + PD-L1 co-localization
3. Proximity ligation assay (PLA): Interaction within <40 nm

---

## Story 3: "Which p62 domain is responsible for PD-L1 sequestration?"

**As a:** Structural biologist designing mutants
**I want to:** Map the minimal domain for p62-PD-L1 interaction
**So that:** I can create separation-of-function mutants

**Acceptance Criteria:**
- [ ] Test p62 domain deletions: ΔPUB, ΔZZ, ΔUBA
- [ ] Measure PD-L1 co-IP in each mutant
- [ ] FRAP analysis: Mobility in condensates
- [ ] Expected: ΔUBA loses PD-L1 binding (ubiquitin-dependent)

**Predicted Outcome (from AlphaFold-Multimer):**
- UBA domain binds PD-L1 via ubiquitin chains
- PB1 domain drives oligomerization (scaffold)
- ZZ domain dispensable for PD-L1

**Validation Tools:**
1. AlphaFold-Multimer: Predict binding interface
2. FoldX: Mutation effects (ΔΔG calculations)
3. Conservation analysis: Identify critical residues

---

## Story 4: "Can we drug the p62-PD-L1 interaction?"

**As a:** Drug discovery scientist
**I want to:** Identify small molecules disrupting p62-PD-L1 condensates
**So that:** I can modulate PD-L1 stability therapeutically

**Acceptance Criteria:**
- [ ] Virtual screening: Dock compounds into p62-PD-L1 interface
- [ ] In vitro screening: Test top 100 compounds in turbidity assay
- [ ] IC50 measurement: Concentration to dissolve condensates
- [ ] Cell-based validation: PD-L1 stability in treated cells
- [ ] Expected: Find 1-3 hits with IC50 <10 μM

**Predicted Outcome:**
- Target p62 PB1 homo-oligomerization interface
- Small molecules disrupt condensate formation
- Result: PD-L1 released to STUB1-mediated degradation

**Validation Tools:**
1. AlphaFold structure: Identify druggable pockets
2. Hexanediol as positive control (but toxic)
3. Optogenetic as orthogonal validation (Cry2 system)

---

## Story 5: "Is this mechanism conserved across species?"

**As a:** Evolutionary biologist
**I want to:** Test if p62-PD-L1 LLPS is conserved in mouse
**So that:** I can validate in preclinical models

**Acceptance Criteria:**
- [ ] Run LLPS prediction on mouse p62 (UniProt Q64337)
- [ ] Run LLPS prediction on mouse PD-L1 (UniProt Q9EP73)
- [ ] Test co-condensation in vitro (mouse proteins)
- [ ] Mouse tumor models: p62 KO + anti-PD-1 therapy
- [ ] Expected: Mechanism conserved if mouse shows same phenotype

**Predicted Outcome (from Seq2Phase multi-species):**
- Human p62 PB1: 89% identical to mouse
- Human PD-L1 tail: 72% identical to mouse
- Hypothesis: Core mechanism conserved

**Validation Tools:**
1. Seq2Phase: Cross-species LLPS prediction
2. Phylogenetic conservation: IDR regions conserved?
3. Patient-derived xenografts (PDX): Human tumors in mice

