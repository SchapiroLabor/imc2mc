# imc2mc
Formatting Imaging Mass Cytrometry (IMC) output files to be compatible with the MCMICRO pipeline.

## Description
**Raw data:** The Hyperion imaging system outputs one .mcd file per slide containing multiple acquisitions as well as one .txt file per acquisition. This script currently uses the .txt files to create a float32 .tif file with corresponding OME-XML metadata per acquisition.
**Steps in this module:**
* create .tif file from .txt file
* add OME-XML metadata to .tif file

## Usage 

### CLI
#### Input
The CLI script `scripts/imc2mc.py` requires 3 inputs
* The path to the acquisition .txt file with `-i` or `--indir`
* The pixel size in um with  `-p` or `--pixel_size`
* The output folder to store the output .tif files in with `-o` or `--outdir`. Will be created if not present.

