#!/usr/bin/env Rscript
#
# Quick Install - Only IOBR for Phase 2B
#

cat("\n================================================================================\n")
cat("QUICK INSTALL - IOBR ONLY\n")
cat("================================================================================\n\n")

# Set user library
user_lib <- path.expand("~/R/library")
dir.create(user_lib, showWarnings = FALSE, recursive = TRUE)
.libPaths(c(user_lib, .libPaths()))

options(repos = c(CRAN = "https://cloud.r-project.org/"))

# Install BiocManager
if (!requireNamespace("BiocManager", quietly = TRUE)) {
  cat("[INSTALL] BiocManager...\n")
  install.packages("BiocManager")
}

cat("\n[INSTALL] IOBR from Bioconductor...\n\n")

# Try to install IOBR
tryCatch({
  BiocManager::install("IOBR", update = FALSE, ask = FALSE)
  cat("\n✅ IOBR installation completed!\n")
  quit(status = 0)
}, error = function(e) {
  cat("\n❌ IOBR installation failed:\n")
  cat(as.character(e), "\n")
  quit(status = 1)
})
