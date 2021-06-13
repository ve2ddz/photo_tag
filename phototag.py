#!
# -*- coding: utf-8 -*-

import math
import exiftool
#from collections import namedtuple

# Get args
image_date = '2020-06-25'
sota_pre = 'VE2'
sota_suf = 'LR-005'
sota_summit = 'Montagne Noire'

park_name = None
wwff = None

#image_directory = '.'
image_directory = 'sample'
n_images = 99

additional_keywords = [
    'Sentier Inter-Centre'
]

# Computed
d_images = int(math.log10(n_images)+1)
image_date_string = image_date

image_filename_template= ' '.join([
    'SOTA',
    sota_pre+'_'+sota_suf,
    sota_summit,
    image_date_string,
    f'%1.{d_images}C.%le'
])

keywords = [
    'SOTA',
    sota_suf,
    sota_summit,
]

tagslist = [
    'SOTA',
    sota_pre+'/'+sota_suf,
    sota_summit,
]

if wwff is not None:
    additional_keywords.append('WWFF')
    keywords.append(wwff)
    tagslist.append('WWFF/'+wwff)
if park_name is not None:
    additional_keywords.append(park_name)
keywords += additional_keywords
tagslist += additional_keywords

constant_tags = {
    'OwnerName':'Malcolm Harper',
    'IFD0:Artist':'Malcolm Harper',
    'IPTC:By-line':'Malcolm Harper',
    'XMP-dc:Creator':'Malcolm Harper',
    'IPTC:By-lineTitle':'Photographer',
    'XMP-photoshop:AuthorsPosition':'Photographer',
    'XMP-photoshop:Credit':'Malcolm Harper, VE2DDZ',
    'IPTC:Contact':'email: ve2ddz@ve2ddz.ca',
    'XMP-iptcCore:CreatorWorkEmail':'ve2ddz@ve2ddz.ca',
}

constant_raw_args = {
    '-IFD0:Copyright<CC BY-NC-SA 2.5 CA ${createdate#;DateFmt("%Y")} Malcolm Harper', 
    '-IPTC:CopyrightNotice<Copyright ${createdate#;DateFmt("%Y")} CC BY-NC-SA 2.5 CA, Malcolm Harper', 
    '-XMP-dc:Rights<CC BY-NC-SA 2.5 CA ${createdate#;DateFmt("%Y")} Malcolm Harper', 
}

tags = { **constant_tags ,'keywords':keywords,'tagslist':tagslist}
raw_args = constant_raw_args

et = exiftool.ExifTool(common_args = ['-G','-n', '-overwrite_original','-P'])
et.start()

# Commands other than tag operations require execute
print('renaming and creation times')
result = et.execute(
    ('-filename='+image_filename_template).encode('utf-8'),
    '-filemodifydate<createdate'.encode('utf-8'),
    image_directory.encode('utf-8')
)
print(result)

# Tag operations can be done using the higher level command.
# getting exiftool to do the batching by passing a directory is much faster.
print()
print('Setting tags')
result = et.set_tags(tags, image_directory)
print(result)

# tags from tags need to be done using raw args
print()
print('Setting tags computed from other tags')
result = et.execute(*[\
    item.encode('utf-8') for item in raw_args],\
    image_directory.encode('utf-8'))
print(result)

# Finally geotag
print()
print('Geotagging')
result = et.execute(\
#    ('-geotag='+image_directory+'/SOTA VE2_LR-005 Montagne Noire 2020-06-25.gpx').encode('utf-8'),\
    '-geotag'.encode('utf-8'), (image_directory+'/*.*x').encode('utf-8'),\
#    '-geotag'.encode('utf-8'), (image_directory+'/*.tcx').encode('utf-8'),\
#    ('-geotag '+image_directory+'/*.tcx').encode('utf-8'),\
    '-geotime<${createdate}-04:00'.encode('utf-8'),\
    image_directory.encode('utf-8'))
print(result)

et.terminate()
