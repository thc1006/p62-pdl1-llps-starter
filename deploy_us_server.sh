#!/bin/bash
################################################################################
# US SERVER DEPLOYMENT SCRIPT
# Automated setup for PD-L1 research pipeline execution
#
# Usage:
#   bash deploy_us_server.sh
#
# This script will:
#   1. Check system requirements
#   2. Install dependencies (Python + R + gdc-client)
#   3. Execute full pipeline automatically
#
# Date: 2025-11-02
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

################################################################################
# Step 0: Pre-flight Checks
################################################################################

log_info "Starting US server deployment..."
log_info "Current directory: $(pwd)"
log_info "Current user: $(whoami)"
log_info "OS: $(uname -s)"

# Check if we're in the right directory
if [[ ! -f "MASTER_EXECUTE_ALL.py" ]]; then
    log_error "MASTER_EXECUTE_ALL.py not found!"
    log_error "Please run this script from the project root directory."
    exit 1
fi

# Check disk space (need at least 100GB)
AVAILABLE_GB=$(df -BG . | tail -1 | awk '{print $4}' | sed 's/G//')
log_info "Available disk space: ${AVAILABLE_GB}GB"

if [[ $AVAILABLE_GB -lt 100 ]]; then
    log_warning "Low disk space! Need at least 100GB, have ${AVAILABLE_GB}GB"
    read -p "Continue anyway? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_error "Aborted by user"
        exit 1
    fi
fi

################################################################################
# Step 1: Install System Dependencies
################################################################################

log_info "Step 1: Installing system dependencies..."

# Detect OS
if [[ -f /etc/os-release ]]; then
    . /etc/os-release
    OS=$ID
    log_info "Detected OS: $OS"
else
    log_warning "Cannot detect OS, assuming Ubuntu/Debian"
    OS="ubuntu"
fi

# Install based on OS
case $OS in
    ubuntu|debian)
        log_info "Installing for Ubuntu/Debian..."
        sudo apt-get update -qq
        sudo apt-get install -y -qq \
            python3 python3-pip python3-venv \
            r-base r-base-dev \
            wget curl unzip \
            build-essential \
            libcurl4-openssl-dev libssl-dev libxml2-dev
        ;;
    centos|rhel|fedora)
        log_info "Installing for CentOS/RHEL/Fedora..."
        sudo yum install -y \
            python3 python3-pip \
            R R-devel \
            wget curl unzip \
            gcc gcc-c++ make \
            libcurl-devel openssl-devel libxml2-devel
        ;;
    *)
        log_warning "Unsupported OS: $OS"
        log_warning "Please install manually: Python 3.11+, R 4.3+, wget, curl, unzip"
        ;;
esac

log_success "System dependencies installed"

################################################################################
# Step 2: Install Python Dependencies
################################################################################

log_info "Step 2: Installing Python dependencies..."

# Create virtual environment
if [[ ! -d "venv" ]]; then
    log_info "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip -q

# Install requirements
if [[ -f "requirements.txt" ]]; then
    log_info "Installing Python packages from requirements.txt..."
    pip install -r requirements.txt -q
else
    log_info "Installing essential Python packages..."
    pip install -q \
        requests pandas numpy scipy matplotlib seaborn \
        statsmodels lifelines pingouin openpyxl
fi

log_success "Python dependencies installed"

################################################################################
# Step 3: Install R Dependencies
################################################################################

log_info "Step 3: Installing R dependencies..."

# Create R installation script
cat > /tmp/install_r_packages.R <<'EOF'
# Set CRAN mirror
options(repos = c(CRAN = "https://cloud.r-project.org"))

# Install CRAN packages
cran_packages <- c(
    "survival", "ggplot2", "dplyr", "tidyr",
    "cowplot", "survminer", "BiocManager"
)

for (pkg in cran_packages) {
    if (!require(pkg, character.only = TRUE)) {
        cat(sprintf("Installing %s...\n", pkg))
        install.packages(pkg, quiet = TRUE)
    } else {
        cat(sprintf("%s already installed\n", pkg))
    }
}

# Install Bioconductor packages
bioc_packages <- c("immunedeconv")

BiocManager::install(bioc_packages, update = FALSE, ask = FALSE)

cat("\nAll R packages installed successfully!\n")
EOF

# Run R installation
Rscript /tmp/install_r_packages.R

log_success "R dependencies installed"

################################################################################
# Step 4: Install gdc-client
################################################################################

log_info "Step 4: Installing gdc-client..."

# Check if already installed
if command -v gdc-client &> /dev/null; then
    log_success "gdc-client already installed: $(which gdc-client)"
else
    log_info "Downloading gdc-client..."

    # Download
    wget -q https://gdc.cancer.gov/files/public/file/gdc-client_v1.6.1_Ubuntu_x64.zip

    # Extract
    unzip -q gdc-client_v1.6.1_Ubuntu_x64.zip

    # Make executable
    chmod +x gdc-client

    # Move to /usr/local/bin
    sudo mv gdc-client /usr/local/bin/

    # Clean up
    rm -f gdc-client_v1.6.1_Ubuntu_x64.zip

    log_success "gdc-client installed to /usr/local/bin/gdc-client"
fi

# Verify
gdc-client --version

################################################################################
# Step 5: Final Checks
################################################################################

log_info "Step 5: Running final checks..."

# Check Python version
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
log_info "Python version: $PYTHON_VERSION"

# Check R version
R_VERSION=$(R --version | head -1 | awk '{print $3}')
log_info "R version: $R_VERSION"

# Check gdc-client
GDC_VERSION=$(gdc-client --version 2>&1 | head -1)
log_info "gdc-client: $GDC_VERSION"

# Check disk space again
AVAILABLE_GB=$(df -BG . | tail -1 | awk '{print $4}' | sed 's/G//')
log_info "Available disk space: ${AVAILABLE_GB}GB"

################################################################################
# Step 6: Ready to Execute
################################################################################

echo ""
echo "========================================================================"
echo "  DEPLOYMENT COMPLETE - READY TO EXECUTE"
echo "========================================================================"
echo ""
log_success "All dependencies installed successfully!"
echo ""
echo "Next steps:"
echo ""
echo "  1. Review the pipeline configuration:"
echo "     cat QUICK_START.md"
echo ""
echo "  2. Execute the full pipeline (4-10 hours):"
echo "     python MASTER_EXECUTE_ALL.py --auto-yes 2>&1 | tee execution.log"
echo ""
echo "  3. Monitor progress in another terminal:"
echo "     tail -f outputs/execution_logs/master_execution_*.log"
echo ""
echo "  4. After completion, verify results:"
echo "     cat outputs/execution_logs/execution_report_*.json"
echo ""
echo "Expected outputs:"
echo "  - outputs/tcga_full_cohort_real/"
echo "  - outputs/figures_publication/"
echo "  - outputs/submission_package/*.zip"
echo ""
echo "========================================================================"
echo ""

# Ask if user wants to start now
read -p "Start execution now? (y/n): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    log_info "Starting pipeline execution..."
    python MASTER_EXECUTE_ALL.py --auto-yes 2>&1 | tee execution.log
else
    log_info "Pipeline execution skipped. Run manually when ready:"
    log_info "  python MASTER_EXECUTE_ALL.py --auto-yes"
fi

################################################################################
# Done
################################################################################

log_success "Deployment script completed!"
