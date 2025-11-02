#!/usr/bin/env Rscript
#
# TIMER2.0 Immune Deconvolution
# Calculates immune cell type fractions from bulk RNA-seq
#
# Input: Expression matrix (genes x samples)
# Output: Immune cell fractions for 6 cell types
#
# Author: Automated Pipeline
# Date: 2025-11-02
#

library(IOBR)
library(tidyverse)

# =============================================================================
# Configuration
# =============================================================================

# Get BASE_DIR for command-line execution
if (interactive() && requireNamespace("rstudioapi", quietly = TRUE)) {
  # Running in RStudio
  BASE_DIR <- dirname(dirname(dirname(rstudioapi::getActiveDocumentContext()$path)))
} else {
  # Running from command line - use script location or working directory
  script_path <- commandArgs(trailingOnly = FALSE)
  file_arg <- grep("^--file=", script_path, value = TRUE)
  if (length(file_arg) > 0) {
    script_file <- sub("^--file=", "", file_arg)
    BASE_DIR <- dirname(dirname(dirname(script_file)))
  } else {
    BASE_DIR <- getwd()
  }
}

# Fallback to working directory if BASE_DIR is invalid
if (BASE_DIR == "" || is.na(BASE_DIR) || !dir.exists(BASE_DIR)) {
  BASE_DIR <- getwd()
}

INPUT_DIR <- file.path(BASE_DIR, "outputs", "tcga_full_cohort_real")
OUTPUT_DIR <- file.path(BASE_DIR, "outputs", "timer2_results")

dir.create(OUTPUT_DIR, recursive = TRUE, showWarnings = FALSE)

# =============================================================================
# Step 1: Load Expression Data
# =============================================================================

cat("\n")
cat("==============================================================================\n")
cat("TIMER2.0 IMMUNE DECONVOLUTION PIPELINE\n")
cat("==============================================================================\n")

cat("\n[LOAD] Reading expression matrix...\n")

expr_file <- file.path(INPUT_DIR, "expression_matrix_full_real.csv")

if (!file.exists(expr_file)) {
  stop(paste0("Expression matrix not found: ", expr_file))
}

expr_df <- read_csv(expr_file, show_col_types = FALSE)

cat(sprintf("  Loaded: %d samples x %d variables\n", nrow(expr_df), ncol(expr_df)))

# =============================================================================
# Step 2: Prepare Expression Matrix
# =============================================================================

cat("\n[PREPARE] Formatting expression matrix for TIMER2.0...\n")

# Extract metadata columns
sample_id <- expr_df$sample_id
cancer_type <- expr_df$cancer_type

# Remove metadata columns
expr_matrix <- expr_df %>%
  select(-sample_id, -cancer_type)

# Transpose to genes x samples
expr_matrix <- t(expr_matrix)
colnames(expr_matrix) <- sample_id

cat(sprintf("  Matrix: %d genes x %d samples\n", nrow(expr_matrix), ncol(expr_matrix)))

# =============================================================================
# Step 2.5: Convert Ensembl IDs to Gene Symbols
# =============================================================================

cat("\n[ANNOTATE] Converting Ensembl IDs to gene symbols...\n")

# Check if rownames are Ensembl IDs
if (grepl("^ENSG", rownames(expr_matrix)[1])) {
  cat("  Detected Ensembl IDs, converting to gene symbols...\n")

  # Use IOBR's anno_eset function with built-in annotation
  # probe="id" means rownames are Ensembl IDs
  expr_matrix <- anno_eset(
    eset = expr_matrix,
    annotation = anno_grch38,
    probe = "id"
  )

  cat(sprintf("  [OK] Converted to gene symbols: %d genes x %d samples\n",
              nrow(expr_matrix), ncol(expr_matrix)))
} else {
  cat("  Gene symbols detected, no conversion needed\n")
}

# =============================================================================
# Step 3: Run TIMER2.0 Deconvolution
# =============================================================================

cat("\n[DECONVOLUTE] Running TIMER2.0...\n")

# TIMER2.0 cell types:
# - B_cell: B cells
# - T_cell.CD4: CD4+ T cells
# - T_cell.CD8: CD8+ T cells
# - Neutrophil: Neutrophils
# - Macrophage: Macrophages
# - Myeloid.dendritic: Dendritic cells

tryCatch({
  # Prepare cancer type indications for TIMER2.0
  # TIMER requires cancer type codes (lowercase) for each sample
  indications <- tolower(cancer_type)

  cat(sprintf("  Cancer types: %s\n", paste(unique(indications), collapse = ", ")))

  # Run TIMER2.0 deconvolution
  timer_results <- deconvo_timer(
    eset = expr_matrix,
    indications = indications  # Cancer type for each sample (required)
  )

  cat("  [OK] TIMER2.0 deconvolution completed\n")

  # Convert to data frame
  timer_df <- as.data.frame(timer_results)
  timer_df$sample_id <- rownames(timer_df)

  # Merge with cancer type
  cancer_type_df <- data.frame(
    sample_id = sample_id,
    cancer_type = cancer_type
  )

  timer_df <- timer_df %>%
    left_join(cancer_type_df, by = "sample_id")

  cat(sprintf("  Cell types quantified: %d\n", ncol(timer_df) - 2))

  # Summary statistics
  cat("\n  Cell type fraction summary:\n")
  for (cell_type in colnames(timer_df)[!colnames(timer_df) %in% c("sample_id", "cancer_type")]) {
    mean_frac <- mean(timer_df[[cell_type]], na.rm = TRUE)
    sd_frac <- sd(timer_df[[cell_type]], na.rm = TRUE)
    cat(sprintf("    %s: %.3f +/- %.3f\n", cell_type, mean_frac, sd_frac))
  }

}, error = function(e) {
  cat(sprintf("  [ERROR] TIMER2.0 failed: %s\n", e$message))
  cat("  [FALLBACK] Using alternative deconvolution method...\n")

  # Fallback to xCell if TIMER2.0 fails
  tryCatch({
    library(xCell)

    xcell_results <- xCellAnalysis(expr_matrix)

    # Select key immune cell types
    key_cells <- c(
      "B-cells", "CD4+ T-cells", "CD8+ T-cells",
      "Neutrophils", "Macrophages", "DC"
    )

    timer_df <- as.data.frame(t(xcell_results[key_cells, ]))
    colnames(timer_df) <- c("B_cell", "T_cell.CD4", "T_cell.CD8",
                            "Neutrophil", "Macrophage", "Myeloid.dendritic")

    timer_df$sample_id <- colnames(expr_matrix)
    timer_df <- timer_df %>%
      left_join(cancer_type_df, by = "sample_id")

    cat("  [OK] xCell deconvolution completed\n")

  }, error = function(e2) {
    cat(sprintf("  [ERROR] xCell also failed: %s\n", e2$message))
    stop("All deconvolution methods failed")
  })
})

# =============================================================================
# Step 4: Calculate Composite Scores
# =============================================================================

cat("\n[CALCULATE] Computing composite immune scores...\n")

# T cell score (CD4+ + CD8+)
timer_df$T_cell_score <- timer_df$T_cell.CD4 + timer_df$T_cell.CD8

# Myeloid score (Macrophage + Neutrophil + DC)
timer_df$Myeloid_score <- timer_df$Macrophage + timer_df$Neutrophil + timer_df$Myeloid.dendritic

# Total immune infiltration
immune_cols <- c("B_cell", "T_cell.CD4", "T_cell.CD8",
                "Neutrophil", "Macrophage", "Myeloid.dendritic")
timer_df$Total_immune <- rowSums(timer_df[, immune_cols])

# Tumor purity (inverse of immune infiltration)
timer_df$Tumor_purity <- 1 - timer_df$Total_immune

cat("  [OK] Composite scores calculated\n")

# =============================================================================
# Step 5: Calculate T-cell Inflamed GEP
# =============================================================================

cat("\n[GEP] Calculating T-cell inflamed gene expression profile...\n")

# 18-gene signature from Ayers et al. 2017 (excluding CD274)
gep_genes <- c(
  "PSMB10", "HLA-DQA1", "HLA-DRB1", "CMKLR1", "HLA-E",
  "NKG7", "CD8A", "CCL5", "CXCL9", "CD27", "CXCR6",
  "IDO1", "STAT1", "TIGIT", "LAG3", "CD276", "PDCD1LG2"
)

# Check which genes are available
available_gep_genes <- gep_genes[gep_genes %in% rownames(expr_matrix)]

cat(sprintf("  Available GEP genes: %d/%d\n", length(available_gep_genes), length(gep_genes)))

if (length(available_gep_genes) >= 10) {
  # Calculate mean expression across GEP genes
  gep_expr <- expr_matrix[available_gep_genes, , drop = FALSE]
  gep_score <- colMeans(gep_expr, na.rm = TRUE)

  # Add to results
  timer_df$GEP_score <- gep_score[timer_df$sample_id]

  cat("  [OK] GEP score calculated\n")
} else {
  cat("  [WARN] Insufficient GEP genes, using T cell score as proxy\n")
  timer_df$GEP_score <- timer_df$T_cell_score
}

# =============================================================================
# Step 6: Save Results
# =============================================================================

cat("\n[SAVE] Writing results...\n")

# Save full results
output_file <- file.path(OUTPUT_DIR, "timer2_immune_scores.csv")
write_csv(timer_df, output_file)
cat(sprintf("  [OK] Saved: %s\n", output_file))

# Save summary by cancer type
summary_df <- timer_df %>%
  group_by(cancer_type) %>%
  summarise(
    n_samples = n(),
    B_cell_mean = mean(B_cell, na.rm = TRUE),
    CD4_T_mean = mean(T_cell.CD4, na.rm = TRUE),
    CD8_T_mean = mean(T_cell.CD8, na.rm = TRUE),
    Neutrophil_mean = mean(Neutrophil, na.rm = TRUE),
    Macrophage_mean = mean(Macrophage, na.rm = TRUE),
    DC_mean = mean(Myeloid.dendritic, na.rm = TRUE),
    Total_immune_mean = mean(Total_immune, na.rm = TRUE),
    Tumor_purity_mean = mean(Tumor_purity, na.rm = TRUE),
    GEP_mean = mean(GEP_score, na.rm = TRUE)
  )

summary_file <- file.path(OUTPUT_DIR, "timer2_summary_by_cancer.csv")
write_csv(summary_df, summary_file)
cat(sprintf("  [OK] Saved: %s\n", summary_file))

# =============================================================================
# Step 7: Summary
# =============================================================================

cat("\n")
cat("==============================================================================\n")
cat("TIMER2.0 DECONVOLUTION COMPLETE\n")
cat("==============================================================================\n")

cat("\nResults summary:\n")
print(summary_df, n = Inf)

cat("\n==============================================================================\n")
cat("Next step:\n")
cat("  Run: python scripts/excellence_upgrade/stage3_v3_timer2_confounders.py\n")
cat("==============================================================================\n")
