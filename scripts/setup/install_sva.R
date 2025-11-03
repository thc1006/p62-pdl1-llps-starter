if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager", repos = "https://cloud.r-project.org")

BiocManager::install("sva", update = FALSE, ask = FALSE)

# Verify installation
library(sva)
cat("sva version:", as.character(packageVersion("sva")), "\n")
