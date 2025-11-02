#!/usr/bin/env Rscript
#
# Install Required R Packages for PD-L1 Pipeline
# Installs IOBR, tidyverse, and other dependencies
#

cat("\n")
cat("================================================================================\n")
cat("R PACKAGE INSTALLATION - PD-L1 PIPELINE\n")
cat("================================================================================\n")
cat("\n")

# Set user library path
user_lib <- path.expand("~/R/library")
dir.create(user_lib, showWarnings = FALSE, recursive = TRUE)
.libPaths(c(user_lib, .libPaths()))

cat("[INFO] Using R library path:", user_lib, "\n")

# Set CRAN mirror
options(repos = c(CRAN = "https://cloud.r-project.org/"))

# Install BiocManager if not available
if (!requireNamespace("BiocManager", quietly = TRUE)) {
  cat("[INSTALL] Installing BiocManager...\n")
  install.packages("BiocManager", quiet = FALSE)
}

cat("\n[CHECK] BiocManager version: ", as.character(BiocManager::version()), "\n")

# List of required packages
packages <- c(
  # Core analysis packages
  "tidyverse",      # Data manipulation
  "dplyr",          # Data wrangling
  "ggplot2",        # Plotting
  "readr",          # File reading

  # Bioconductor packages for immune analysis
  "IOBR",           # Immune deconvolution (TIMER2.0)
  "immunedeconv",   # Multiple deconvolution methods

  # Statistical packages
  "survival",       # Survival analysis
  "survminer"       # Survival plotting
)

cat("\n")
cat("================================================================================\n")
cat("INSTALLING PACKAGES\n")
cat("================================================================================\n")
cat("\n")

# Install CRAN packages first
cran_packages <- c("tidyverse", "dplyr", "ggplot2", "readr", "survival", "survminer")
for (pkg in cran_packages) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    cat(sprintf("[INSTALL] %s from CRAN...\n", pkg))
    install.packages(pkg, quiet = FALSE)
  } else {
    cat(sprintf("[OK] %s already installed\n", pkg))
  }
}

# Install Bioconductor packages
bioc_packages <- c("IOBR", "immunedeconv")
for (pkg in bioc_packages) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    cat(sprintf("[INSTALL] %s from Bioconductor...\n", pkg))
    BiocManager::install(pkg, update = FALSE, ask = FALSE)
  } else {
    cat(sprintf("[OK] %s already installed\n", pkg))
  }
}

cat("\n")
cat("================================================================================\n")
cat("VERIFYING INSTALLATIONS\n")
cat("================================================================================\n")
cat("\n")

# Verify all packages
success <- TRUE
for (pkg in packages) {
  if (requireNamespace(pkg, quietly = TRUE)) {
    version <- tryCatch(
      as.character(packageVersion(pkg)),
      error = function(e) "unknown"
    )
    cat(sprintf("[OK] %-20s %s\n", pkg, version))
  } else {
    cat(sprintf("[FAIL] %-20s NOT INSTALLED\n", pkg))
    success <- FALSE
  }
}

cat("\n")
if (success) {
  cat("✅ All packages installed successfully!\n")
  quit(status = 0)
} else {
  cat("❌ Some packages failed to install\n")
  quit(status = 1)
}
