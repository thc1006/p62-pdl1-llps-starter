# Dockerfile for Excellence Upgrade Pipeline
FROM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y build-essential curl git && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install --no-cache-dir pandas==1.4.4 numpy==1.23.5 scipy==1.9.3 matplotlib==3.6.2 seaborn==0.12.1 lifelines==0.27.4 scikit-learn==1.1.3 statsmodels==0.13.5 reportlab==3.6.12 Pillow==9.3.0 pingouin==0.5.3 tqdm==4.64.1

WORKDIR /project
COPY . /project
CMD ["bash"]
