# notes:




```python
>>> image_directory = os.scandir('sample')
>>> for fn in image_directory:
...     print(fn)
```
gives a list of the directory
```python
>>> for fn in image_directory:
...     print(fn)
```
gives nothing as the iterable is exhausted

```python
>>> with os.scandir('sample') as image_directory:
...     n_images = sum(filetype.is_image(filename.path) or filetype.is_video(filename.path) for filename in image_directory)
...     gpstraces = fnmatch.filter(image_directory,'*.gpx')

n_images gives correct count, but gpstraces is [], because _the iterable is exhausted_

```python
>>> with os.scandir('sample') as image_directory:
...     gpstraces = fnmatch.filter(image_directory,'*.gpx')
print(gpstraces)
```
`[<DirEntry 'SOTA VE2_LR-081 Mont Bondy 2021-07-11.gpx'>]`
`print(gpstraces[0].path)`: `sample\SOTA VE2_LR-081 Mont Bondy 2021-07-11.gpx`
