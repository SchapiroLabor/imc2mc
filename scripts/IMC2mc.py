#!/usr/bin/env python
########################################################################################################
# AUTHOR: Margot Chazotte <margot.chazotte@gmail.com>
# DESCRIPTION: Convert Image Mass Cytometry (IMC) output .txt files to a .tif file with correct OME-XML metadata
########################################################################################################

from readimc import TXTFile
import ome_types
from ome_types.model import OME,Pixels,TiffData,Channel,Plane
from ome_types.model.simple_types import PixelsID
from ome_types.model.pixels import DimensionOrder
from ome_types import to_xml
import tifffile as tiff
import copy
import platform
from uuid import uuid4
import argparse
import os
from pathlib import Path


#---CLI-BLOCK---#
def getOptions(myopts=None):
    """ Function to pull in arguments """
    description = """ IMC2MC """
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    # Standard Input
    standard = parser.add_argument_group(
        title='Standard Inputs',
        description='Standard input for staging module.')
    # provide input .txt file    ## TODO: potentially change to input folder containing multiple txt files, depending on nextflow
    standard.add_argument(
        "-i",
        "--input",
        dest="input",
        action='store',
        required=True,
        help="Input .txt file from IMC.") #Input folder with .txt files from IMC. txt files need to contain image in cyx format!
    standard.add_argument(
        "-p",
        "--pixel_size",
        dest="pixel_size",
        action="store",
        required=True,
        type=int,
        help="Provide pixel size in um.")

    # Tool Output
    output = parser.add_argument_group(title='Required output')
    output.add_argument(
        "-o",
        "--outdir",
        dest="outdir",
        action='store',
        required=True,
        help="Output directory, will be created if non existent.")

    args = parser.parse_args(myopts)

    # Standardize paths
    args.input = os.path.abspath(args.input)
    return (args)
#---END_CLI-BLOCK---#


#----HELPER-FUNCTIONS----#
# create tiff file from input txt file and define global input derived variables 
def create_tiff(input_file, output_file):
    """
    Read acquisition txt file and create tiff file 

    :Arguments:
        :type input_file: txt file
        :param input_file: txt file containing acquisition data

        :type output_file: .tif file
        :param output_file: file to save the output .tif file
    """
    with TXTFile(input_file) as f:
        global markers
        markers = f.channel_labels # targets
        global img  ## TODO: save only shape as global variable here to save memory
        img = f.read_acquisition() # numpy array, shape: (c,y,x), dtype: float32  
    tiff.imwrite(output_file, img)


# create OME-XML metadata and add to tiff file
def create_ome(pixel_size, output_file):
    """
    Creates and overwrites correct omexml metadata for the OME-TIFF files

    :Arguments:
        :type pixel_size: integer
        :param pixel_size: Pixel size in um.

        :type output_file: tif file
        :param output_file: file to save the output .tif file with OME-XML metadata
    """    
    #--Define variables--#
    no_of_channels = img.shape[0]
    no_of_tiles = 1 #hard coded for now 
    #bits_per_sample = 32
    pixel_size = pixel_size

    #--Generate channels block--#
    chann_block = []
    for ch, chann_name in enumerate(markers):
        chann_block.append(
            Channel(
                id=ome_types.model.simple_types.ChannelID(
                    'Channel:{x}'.format(x=ch)),
                    name=chann_name
                    ))
        
    #--Generate tiff_data_blocks--#
    tiff_block = []
    #uuid_obj=UUID(file_name=img_name,value=uuid4().urn)
    for ch in range(0, no_of_channels):
        tiff_block.append(
            TiffData(
                first_c=ch,
                ifd=ch,
                plane_count=1  #,
                #uuid=uuid_obj
            ))
        
    #--Generate planes block (contains the information of each tile)--#
    plane_block = []
    #length_units=ome_types.model.simple_types.UnitsLength('µm')
    for ch in range(0, no_of_channels):
        plane_block.append(
            Plane(
                the_c=ch,
                the_t=0,
                the_z=0
            ))    
        
    #--Generate pixels block--#
    pix_block = []
    ifd_counter = 0
    for t in range(0, no_of_tiles):
        template_plane_block = copy.deepcopy(plane_block)
        template_chann_block = copy.deepcopy(chann_block)
        template_tiffdata_block = copy.deepcopy(tiff_block)
        for ch, mark in enumerate(markers):
            template_chann_block[ch].id = 'Channel:{y}:{x}'.format(x=ch,y=100 +t)  ### why?
            template_chann_block[ch].name = mark
            template_tiffdata_block[ch].ifd = ifd_counter
            ifd_counter += 1
        pix_block.append(
            Pixels(
                id=ome_types.model.simple_types.PixelsID('Pixels:{x}'.format(x=t)),
                dimension_order=ome_types.model.pixels.DimensionOrder('XYZCT'),  ### check if the order is correct!!
                size_c=no_of_channels,
                size_t=1,
                size_x=img.shape[2],
                size_y=img.shape[1],
                size_z=1,
                type=ome_types.model.pixels.PixelType('float'),
                big_endian=False,
                channels=template_chann_block,
                interleaved=False,
                physical_size_x=pixel_size, # hard coded for now 
                physical_size_y=pixel_size, # hard coded for now
                physical_size_z=1.0,
                planes=template_plane_block,
                #bits_per_sample=bits_per_sample,
                tiff_data_blocks=template_tiffdata_block))
        
    #--Generate image block--#
    img_block = []
    for t in range(0, no_of_tiles):
        img_block.append(
            ome_types.model.Image(
                id=ome_types.model.simple_types.ImageID('Image:{x}'.format(x=t)),
                pixels=pix_block[t]))    
        
    #--Create the OME object with all previously defined blocks--#
    ome_custom = OME()
    ome_custom.creator = " ".join([
        ome_types.__name__, ome_types.__version__, '/ python version-',
        platform.python_version()
    ])
    ome_custom.images = img_block
    ome_custom.uuid = uuid4().urn
    ome_xml = to_xml(ome_custom)
    tiff.tiffcomment(output_file, ome_xml)
#----END_HELPER-FUNCTIONS----#


#----MAIN-FUNCTION----#
# create tiff with OME-XML metadata out of acquisition txt file
def main(args):
    """
    Create tiff and add ome-metadata out of .txt file to have one file per acquisition with OME-XML metadata

    :Arguments:
        :type args.input: txt file
        :param args.input: Input txt file containing acquisition data

        :type args.outdir: folder
        :param args.outdir: output folder to save the output .tif file with OME-XML metadata. Will be created if not existent.
        
    """
    # Define output file by adding _output.tif to input file name and create output directory if not already existent
    output_file = Path(args.input).stem + '_output.tif'
    output_file = Path(args.outdir) / output_file
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Read txt file and create tiff and data dependent variables
    create_tiff(args.input, output_file)
    # Create OME-XML metadata and add to tiff file
    create_ome(args.pixel_size, output_file)


if __name__ == '__main__':
     """Tool is called on the command-line"""
     
     args = getOptions()
     #warnings.filterwarnings("ignore", category=DeprecationWarning)  #add if needed
     
     main(args)