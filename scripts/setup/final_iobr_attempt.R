#!/usr/bin/env Rscript
#
# ABSOLUTE FINAL ATTEMPT - Install clusterProfiler, GSVA, and IOBR
#

cat("\n")
cat("================================================================================\n")
cat("ABSOLUTE FINAL ATTEMPT - IOBR INSTALLATION\n")
cat("================================================================================\n")
cat("\n")

user_lib <- path.expand("~/R/library")
.libPaths(c(user_lib, .libPaths()))

options(repos = c(CRAN = "https://cloud.r-project.org/"))

if (!requireNamespace("BiocManager", quietly = TRUE)) {
  install.packages("BiocManager")
}

if (!requireNamespace("remotes", quietly = TRUE)) {
  install.packages("remotes")
}

# Step 1: Install clusterProfiler (if not already)
cat("[STEP 1] Installing clusterProfiler...\n")
tryCatch({
  BiocManager::install("clusterProfiler", update = FALSE, ask = FALSE)
  cat("✅ clusterProfiler installed\n\n")
}, error = function(e) {
  cat("⚠️  clusterProfiler warning:", as.character(e), "\n\n")
})

# Step 2: Install GSVA (if not already)
cat("[STEP 2] Installing GSVA...\n")
tryCatch({
  BiocManager::install("GSVA", update = FALSE, ask = FALSE)
  cat("✅ GSVA installed\n\n")
}, error = function(e) {
  cat("⚠️  GSVA warning:", as.character(e), "\n\n")
})

# Step 3: Verify they're actually installed
cat("[STEP 3] Verifying installations...\n")
cp_ok <- requireNamespace("clusterProfiler", quietly = TRUE)
gsva_ok <- requireNamespace("GSVA", quietly = TRUE)

cat(sprintf("  clusterProfiler: %s\n", ifelse(cp_ok, "✅ OK", "❌ MISSING")))
cat(sprintf("  GSVA: %s\n", ifelse(gsva_ok, "✅ OK", "❌ MISSING")))

if (!cp_ok || !gsva_ok) {
  cat("\n❌ Dependencies still missing, cannot install IOBR\n")
  quit(status = 1)
}

# Step 4: Install IOBR from GitHub
cat("\n[STEP 4] Installing IOBR from GitHub...\n")
tryCatch({
  remotes::install_github("IOBR/IOBR", upgrade = "never", force = TRUE)

  # Verify IOBR
  library(IOBR)

  cat("\n")
  cat("================================================================================\n")
  cat("✅ ✅ ✅ IOBR INSTALLATION SUCCESSFUL! ✅ ✅ ✅\n")
  cat("================================================================================\n")
  quit(status = 0)

}, error = function(e) {
  cat("\n")
  cat("================================================================================\n")
  cat("❌ IOBR INSTALLATION FAILED\n")
  cat("================================================================================\n")
  cat("Error:", as.character(e), "\n")
  quit(status = 1)
})
