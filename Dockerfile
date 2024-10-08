# Use the official micromamba image as a base
FROM mambaorg/micromamba:latest
LABEL maintainer="Margot Chazotte"

# Set the base layer for micromamba and copy the environment file
USER root
COPY environment.yml .

# Update package manager and install essential build tools procps is required for Nextflow/nf-core
RUN apt-get update -qq && apt-get install -y \
    build-essential \
    ffmpeg \
    libsm6 \
    libxext6 \
    procps

# Set the environment variable for the root prefix
ARG MAMBA_ROOT_PREFIX=/opt/conda

# Add /opt/conda/bin to the PATH
ENV PATH $MAMBA_ROOT_PREFIX/bin:$PATH

# Install dependencies with micromamba, clean afterwards
RUN micromamba env create -f environment.yml \
    && micromamba clean --all --yes

# Add environment to PATH
ENV PATH="/opt/conda/envs/imc2mc/bin:$PATH"

# Set the working directory
WORKDIR /imc2mc

# Copy contents of the folder to the working directory
COPY . .