# imc2mc
Formatting Imaging Mass Cytrometry (IMC) output files to be compatible with the MCMICRO pipeline.

## Description
The Hyperion imaging system outputs one .mcd file per slide containing multiple acquisitions as well as one .txt file per acquisition. This script currently uses the .txt files to create a float32 .tif file with corresponding OME-XML metadata per acquisition. To transform the .txt. file to a .tif file we use the [readimc](https://github.com/BodenmillerGroup/readimc) package by BodenmillerGroup. Hot pixel filtering is based on the [Steinbock](https://bodenmillergroup.github.io/steinbock/latest/) pipeline.

**Steps in this module:**
* create .tif file from .txt file
* add OME-XML metadata to .tif file

## Usage 

### CLI
#### Input
The CLI script `imc2mc` requires 3 inputs
* The path to the acquisition .txt file with `-i` or `--input`
* The pixel size in um with  `-p` or `--pixel_size`
* The output .tif file with `-o` or `--output`. Folder structure will be created if not present.

Optional input:
* To apply hot pixel filtering, input an integer with `-t` or `--hp_threshold`. Based on [Steinbock](https://bodenmillergroup.github.io/steinbock/latest/cli/preprocessing/) we recommend a threshold of 50. 
* The current version can be accessed with `-v`or `--version`

## Installation
### Option 1: Install from PyPI
```
pip install imc2mc
imc2mc --help
```

### Option 2: Docker
Pull the image:
```
docker pull ghcr.io/schapirolabor/imc2mc:latest
```
and run the tool directly, mounting your input and output directories:
```
docker run --rm -v $(pwd):/data ghcr.io/schapirolabor/imc2mc:latest \
    imc2mc \
    -i /data/input_dir \
    -o /data/output.ome.tif \
    -p 1 \
    -t 50
```

### Option 3: Development/Conda environment
For development or reproducible research setups:
```
git clone https://github.com/SchapiroLabor/imc2mc.git
cd Background_subtraction
conda env create -f environment.yml
conda activate imc2mc_env

pip install -e .
```
run
```
imc2mc --help
```
