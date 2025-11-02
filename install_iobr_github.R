#!/usr/bin/env Rscript
#
# Install IOBR from GitHub with all dependencies
#

cat("\n")
cat("================================================================================\n")
cat("IOBR INSTALLATION FROM GITHUB\n")
cat("================================================================================\n")
cat("\n")

# Set user library
user_lib <- path.expand("~/R/library")
dir.create(user_lib, showWarnings = FALSE, recursive = TRUE)
.libPaths(c(user_lib, .libPaths()))

cat("[INFO] Using R library path:", user_lib, "\n\n")

options(repos = c(CRAN = "https://cloud.r-project.org/"))

# Step 1: Install BiocManager and devtools
cat("[STEP 1] Installing BiocManager and devtools...\n")
if (!requireNamespace("BiocManager", quietly = TRUE)) {
  install.packages("BiocManager", quiet = FALSE)
}
if (!requireNamespace("devtools", quietly = TRUE)) {
  install.packages("devtools", quiet = FALSE)
}

# Step 2: Install IOBR dependencies
cat("\n[STEP 2] Installing IOBR dependencies...\n")
depens <- c('tibble', 'survival', 'survminer', 'limma', "DESeq2", "devtools",
            'limSolve', 'GSVA', 'e1071', 'preprocessCore', "tidyHeatmap",
            "caret", "glmnet", "ppcor", "timeROC", "pracma", "factoextra",
            "FactoMineR", "WGCNA", "patchwork", 'ggplot2', "biomaRt",
            'ggpubr', "PMCMRplus")

cat(sprintf("  Total dependencies: %d\n", length(depens)))

for(i in 1:length(depens)){
  depen <- depens[i]
  cat(sprintf("  [%d/%d] Checking %s...\n", i, length(depens), depen))

  if (!requireNamespace(depen, quietly = TRUE)) {
    cat(sprintf("        Installing %s...\n", depen))
    tryCatch({
      BiocManager::install(depen, update = FALSE, ask = FALSE)
      cat(sprintf("        ✅ %s installed\n", depen))
    }, error = function(e) {
      cat(sprintf("        ⚠️  %s failed: %s\n", depen, as.character(e)))
    })
  } else {
    cat(sprintf("        ✅ %s already installed\n", depen))
  }
}

# Step 3: Install IOBR from GitHub
cat("\n[STEP 3] Installing IOBR from GitHub...\n")
if (!requireNamespace("IOBR", quietly = TRUE)) {
  cat("  Downloading from GitHub (IOBR/IOBR)...\n")
  tryCatch({
    devtools::install_github("IOBR/IOBR", upgrade = "never")
    cat("\n✅ IOBR installation completed!\n")
  }, error = function(e) {
    cat("\n❌ IOBR installation failed:\n")
    cat(as.character(e), "\n")
    quit(status = 1)
  })
} else {
  cat("  ✅ IOBR already installed\n")
}

# Step 4: Verify installation
cat("\n[STEP 4] Verifying IOBR installation...\n")
if (requireNamespace("IOBR", quietly = TRUE)) {
  cat("✅ IOBR successfully loaded!\n")
  cat("\n")
  cat("================================================================================\n")
  cat("INSTALLATION COMPLETE\n")
  cat("================================================================================\n")
  quit(status = 0)
} else {
  cat("❌ IOBR installation verification failed\n")
  quit(status = 1)
}
