#!/usr/bin/env Rscript
#
# Install IOBR using remotes (lighter than devtools)
#

cat("\n================================================================================\n")
cat("IOBR INSTALLATION USING REMOTES\n")
cat("================================================================================\n\n")

# Set user library
user_lib <- path.expand("~/R/library")
.libPaths(c(user_lib, .libPaths()))

options(repos = c(CRAN = "https://cloud.r-project.org/"))

cat("[INFO] Attempting IOBR installation with remotes package...\n\n")

# Try with remotes
if (!requireNamespace("remotes", quietly = TRUE)) {
  cat("[ERROR] remotes package not found!\n")
  quit(status = 1)
}

cat("✅ remotes package found\n")
cat("[INSTALL] Downloading IOBR from GitHub...\n\n")

tryCatch({
  remotes::install_github("IOBR/IOBR", upgrade = "never", force = FALSE)

  cat("\n[VERIFY] Checking if IOBR can be loaded...\n")
  library(IOBR)

  cat("\n")
  cat("================================================================================\n")
  cat("✅ IOBR INSTALLATION SUCCESSFUL!\n")
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
