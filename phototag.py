#!

import os, os.path  # Needed only to count files (so far)

import math         # Needed only to compute one logarithm (so far)
import argparse

import exiftool

# Get args

parser=argparse.ArgumentParser(
    description = "Front end for tagging phots using exiftool",
    fromfile_prefix_chars='@',
)

parser.add_argument('images',
    help = "Directory (of images) to process",
    default = ".",
)

parser.add_argument('--date',
    help = "Date string for filenames",
)

image_date = '2021-08-15'

parser.add_argument('--sota_ref',
    help = "SOTA reference - required",
)

parser.add_argument('--sota_summit',
    help = "SOTA summit name",
)

#sota_ref = 'VE2/ES-034'

#sota_pre, sota_suf = sota_ref.split("/")

#sota_pre = 'VE2'
#sota_suf = 'ES-034'
#sota_summit = 'Mont des Trois-Lacs'

parser.add_argument('--park',
    help = "Name of location",
    action = 'extend',
    nargs = 1,  # To compensate for a bug, see https://bugs.python.org/issue40365
    default = [],
)

park = None

parser.add_argument('--activity',
    help = "An added activity like WWFF. ACTIVITY/reference",
    action = 'extend',
    nargs = 1,  # To compensate for a bug, see https://bugs.python.org/issue40365
#    type=str,
    default = [],
)

"""
parser.add_argument('wwff',
    help = "WWFF reference",
)

wwff = None

parser.add_argument('pota',
    help = "POTA reference",
)

pota = None

parser.add_argument('qcpota',
    help = "QcPOTA reference",
)

qcpota = None
"""

parser.add_argument('--event',
    help = "Special event name",
    action = 'extend',
    nargs = 1,  # To compensate for a bug, see https://bugs.python.org/issue40365
    default = [],
)

parser.add_argument('--keywords',
    help = "Additional keywords for tagging",
    action = 'extend',
    nargs = '*',  # To compensate for a bug, see https://bugs.python.org/issue40365
    default = [],
)

parser.add_argument('--digits',
    help = "Numer of digits to use when renaming",
    default = None,
)


# event = "Skeeter Hunt"

args = parser.parse_args()

print(args)

image_directory = args.images
d_images = args.digits
additional_keywords = args.keywords

# FIXME
# event is used in the filename template
# There are illegal characters that should be filtered
# some characters can have unexpected results
# For example with 2021/08/15 exiftool will create subdirectories.

event = args.event

if d_images is None:
    d_images  = int(math.log10(len(os.listdir(image_directory)))+1)


# FIXME
# Imagedatestring is used in the filename template
# There are illegal characters that should be filtered
# some characters can have unexpected results
# For example with 2021/08/15 exiftool will create subdirectories.

#image_date_string = image_date
image_date_string = args.date

sota = args.sota_ref
sota_summit = args.sota_summit

if sota:
    sota_ref_cleaned = '_'.join(sota.split('/'))
    image_filename_template= ' '.join([
        'SOTA',
        sota_ref_cleaned,
        sota_summit,
        image_date_string,
        *event,
        f'%1.{d_images}C.%le'
    ])

# FIXME
# Add provision if sota_summit is empty or undefined

keywords = [
    'SOTA',
    sota,
    sota_summit,
]

tagslist = [
    'SOTA',
    sota_ref_cleaned,
    sota_summit,
]

for activity in args.activity:
    activity_category, _, activity_reference = activity.partition('/')
    print(f"{activity_category=} {activity_reference=}")
    additional_keywords.append(activity_category)
    if len(activity_reference):
        additional_keywords.append(activity)

"""
if wwff is not None:
    additional_keywords.append('WWFF')
    keywords.append(wwff)
    tagslist.append('WWFF/'+wwff)
if pota is not None:
    additional_keywords.append('POTA')
    keywords.append(pota)
    tagslist.append('POTA/'+pota)
if qcpota is not None:
    additional_keywords.append('QcPOTA')
    keywords.append(qcpota)
    tagslist.append('QcPOTA/'+qcpota)
if event is not None:
    additional_keywords.append(event)
if park_name is not None:
    additional_keywords.append(park_name)
"""

# for i in [*args.event,*args.park]:
for i in set(args.event + args.park):
    print(f'{i=}')
    additional_keywords.append(i)

keywords += additional_keywords
tagslist += additional_keywords

print(f"{keywords=} {tagslist=}")

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

# FIXME Why is DateTimeOriginal canonical for fileorder, but CreateData is canonical for filemodifydate?
# Geotagging later uses createdate

# TODO enable optional setting of geomaxintsecs in geotagging command

print('renaming and creation times')
result = et.execute(
    '-fileOrder'.encode('utf-8'), 'DateTimeOriginal'.encode('utf-8')    ,
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
result = et.execute(
    '-api'.encode('utf-8'), 'geomaxintsecs=14400'.encode('utf-8'),
#    '-api'.encode('utf-8'), 'geomaxintsecs=25200'.encode('utf-8'),
#    ('-geotag='+image_directory+'/SOTA VE2_LR-005 Montagne Noire 2020-06-25.gpx').encode('utf-8'),\
    '-geotag'.encode('utf-8'), (image_directory+'/*.*x').encode('utf-8'),
#    '-geotag'.encode('utf-8'), (image_directory+'/*.tcx').encode('utf-8'),\
#    ('-geotag '+image_directory+'/*.tcx').encode('utf-8'),\
#    '-geosync=-0:00'.encode('utf-8'),
    '-geosync=-0:58'.encode('utf-8'),
#    '-geotime<${createdate}-04:00'.encode('utf-8'),
    '-geotime<${createdate}-00:00'.encode('utf-8'),
    image_directory.encode('utf-8'))
print(result)

# Close up exiftool process
et.terminate()