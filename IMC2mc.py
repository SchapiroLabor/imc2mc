from readimc import MCDFile, TXTFile
import ome_types
from ome_types.model import OME,Instrument,Pixels,TiffData,Channel,Plane,Pixels_DimensionOrder
from ome_types.model.simple_types import PixelsID
from ome_types.model.pixels import DimensionOrder
from ome_types import to_xml
import tifffile as tiff
from tifffile import imwrite
import copy
import platform
from uuid import uuid4

with TXTFile("IMC_sample/TS-373_IMC01_UB_ROI_2.txt") as f:
    metals = f.channel_names # metals
    markers = f.channel_labels # targets
    img = f.read_acquisition() # numpy array, shape: (c,y,x), dtype: float32
    
imwrite('imc.tif', img )

# define markers
#markers = []
#markers = targets
img_name = "test"
no_of_channels = img.shape[0]
no_of_tiles = 1 #hard coded for now 
bits_per_sample = 32

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

        template_chann_block[ch].id = 'Channel:{y}:{x}'.format(x=ch,
                                                                y=100 +
                                                                t)  ### why?
        template_chann_block[ch].name = mark
        template_tiffdata_block[ch].ifd = ifd_counter
        ifd_counter += 1
    pix_block.append(
        Pixels(
            id=ome_types.model.simple_types.PixelsID(
                'Pixels:{x}'.format(x=t)),
            dimension_order=ome_types.model.pixels.DimensionOrder(
                'XYZCT'),  ### check if the order is correct!!
            size_c=no_of_channels,
            size_t=1,
            size_x=img.shape[2],
            size_y=img.shape[1],
            size_z=1,
            type=ome_types.model.pixels.PixelType('float'),
            big_endian=False,
            channels=template_chann_block,
            interleaved=False,
            physical_size_x=1, # hard coded for now 
            physical_size_y=1, # hard coded for now
            physical_size_z=1.0,
            planes=template_plane_block,
            bits_per_sample=bits_per_sample,
            tiff_data_blocks=template_tiffdata_block))

#--Generate image block--#
img_block = []
for t in range(0, no_of_tiles):
    img_block.append(
        ome_types.model.Image(id=ome_types.model.simple_types.ImageID(
            'Image:{x}'.format(x=t)),
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
tiff.tiffcomment('imc.tif', ome_xml)