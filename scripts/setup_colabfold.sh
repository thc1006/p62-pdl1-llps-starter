#!/bin/bash
# AlphaFold-Multimer Setup Script (ColabFold)
# Run this in WSL with GPU support

echo "🧬 Setting up AlphaFold-Multimer (ColabFold)"
echo "=========================================="

# Check NVIDIA GPU
if ! nvidia-smi &> /dev/null; then
    echo "❌ ERROR: NVIDIA GPU not detected"
    exit 1
fi

echo "✅ GPU detected"
nvidia-smi

# Install ColabFold using Docker
echo "📦 Pulling ColabFold Docker image..."
docker pull ghcr.io/sokrypton/colabfold:latest

# Create output directory
mkdir -p outputs/alphafold_multimer

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run AlphaFold-Multimer predictions:"
echo "docker run --gpus all -v $(pwd):/workspace ghcr.io/sokrypton/colabfold:latest \"
echo "  colabfold_batch \"
echo "  --num-recycle 3 \"
echo "  --amber \"
echo "  /workspace/data/p62_pdl1_sequences.fasta \"
echo "  /workspace/outputs/alphafold_multimer/"
