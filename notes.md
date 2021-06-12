Can geotag using, for example:

```[python]
import exiftool

et = exiftool.ExifTool(common_args = ['-G','-n'])
et.start()

et.execute(b"-overwrite_original",b"-P",b"-geotag = sample/SOTA VE2_LR-017 Vache Noire 2018-03-30.gpx",b"-geotime<${createdate}-05:00",b"sample")
```

I can probably put the `"-overwrite_original", "-P"` into common_args.

common_args:

pyexiftool

* -G
* -n

Me

* -overwrite_original: don't make backupfiles
* -P: keep original times

Run through with new samples

* cull photos manually
* zip to backup photos

```python

import exiftool

et = exiftool.ExifTool(common_args = ['-G', '-n', '-overwrite_original', '-P'])
et.start()
et.execute(b"-filename=SOTA VE2_LR-094 2021-05-24 %1.2C.%le", b"sample")
et.execute(b"-filemodifydate<createdate" , b"sample")
copyright_tags = {
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
et.set_tags(copyright_tags,'sample')
copyright_command = (
    b'-IFD0:Copyright<CC BY-NC-SA 2.5 CA ${createdate#;DateFmt("%Y")} Malcolm Harper', 
    b'-IPTC:CopyrightNotice<Copyright ${createdate#;DateFmt("%Y")} CC BY-NC-SA 2.5 CA, Malcolm Harper', 
    b'-XMP-dc:Rights<CC BY-NC-SA 2.5 CA ${createdate#;DateFmt("%Y")} Malcolm Harper', 
    )
et.execute(*copyright_command, b'sample')

keywords = [
    'SOTA',
    'LR-094',
    'Alléluia Trail',
    ]
tagslist = [
    'SOTA',
    'VE2/LR-094',
    'Alléluia Trail',
    ]
et.set_tags({'keywords':keywords,'tagslist':tagslist},'sample')

# adjust timezone for camera as needed 00:00 UTC, -04:00 EDT, -05:00 EST
et.execute(b'-geotag = sample/SOTA VE2_LR-094 2021-05-24.gpx', b'-geotime<${createdate}-00:00', b'sample')
