# imc2mc
Formatting Imaging Mass Cytrometry (IMC) output files to be compatible with the MCMICRO pipeline.

## Description
The Hyperion imaging system outputs one .mcd file per slide containing multiple acquisitions as well as one .txt file per acquisition. This script currently uses the .txt files to create a float32 .tif file with corresponding OME-XML metadata per acquisition. To transform the .txt. file to a .tif file we use the [readimc](https://github.com/BodenmillerGroup/readimc) package by BodenmillerGroup.

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
* The current version can be accessed with `-v`or `--version`

