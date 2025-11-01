FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime

# Set working directory
WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    wget \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Copy SaProt requirements
COPY tools/SaProt/requirements.txt /tmp/saprot_requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /tmp/saprot_requirements.txt

# Install additional tools
RUN pip install --no-cache-dir \
    requests \
    pandas \
    numpy \
    matplotlib \
    seaborn \
    lifelines \
    pyyaml \
    lxml \
    biopython

# Copy project files
COPY . /workspace/

# Set environment variables
ENV PYTHONPATH=/workspace
ENV TRANSFORMERS_CACHE=/workspace/.cache/huggingface

# Default command
CMD ["/bin/bash"]
