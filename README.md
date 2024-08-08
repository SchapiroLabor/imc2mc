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
The CLI script `scripts/imc2mc.py` requires 3 inputs
* The path to the acquisition .txt file with `-i` or `--input`
* The pixel size in um with  `-p` or `--pixel_size`
* The output folder to store the output .tif files in with `-o` or `--outdir`. Will be created if not present.

Optional input:
* To apply hot pixel filtering, input an integer with `-t` or `--hp_threshold`. Based on [Steinbock](https://bodenmillergroup.github.io/steinbock/latest/cli/preprocessing/) we recommend a threshold of 50. 
* The current version can be accessed with `-v`or `--version`

