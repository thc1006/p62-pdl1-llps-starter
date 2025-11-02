#!/usr/bin/env Rscript
#
# Install 4 missing IOBR dependencies
#

cat("\n================================================================================\n")
cat("INSTALLING 4 MISSING IOBR DEPENDENCIES\n")
cat("================================================================================\n\n")

user_lib <- path.expand("~/R/library")
.libPaths(c(user_lib, .libPaths()))

options(repos = c(CRAN = "https://cloud.r-project.org/"))

if (!requireNamespace("BiocManager", quietly = TRUE)) {
  install.packages("BiocManager")
}

missing_deps <- c("ggpubr", "survminer", "clusterProfiler", "GSVA")

cat(sprintf("[INSTALL] Installing %d missing dependencies...\n\n", length(missing_deps)))

for (dep in missing_deps) {
  cat(sprintf("[%s] Installing...\n", dep))
  tryCatch({
    BiocManager::install(dep, update = FALSE, ask = FALSE)
    cat(sprintf("✅ %s installed\n\n", dep))
  }, error = function(e) {
    cat(sprintf("❌ %s failed: %s\n\n", dep, as.character(e)))
  })
}

# Now try IOBR again
cat("[FINAL ATTEMPT] Installing IOBR from GitHub...\n")
if (!requireNamespace("remotes", quietly = TRUE)) {
  install.packages("remotes")
}

tryCatch({
  remotes::install_github("IOBR/IOBR", upgrade = "never", force = TRUE)
  library(IOBR)
  cat("\n✅ IOBR INSTALLATION SUCCESSFUL!\n")
  quit(status = 0)
}, error = function(e) {
  cat("\n❌ IOBR still failed\n")
  cat("Error:", as.character(e), "\n")
  quit(status = 1)
})
