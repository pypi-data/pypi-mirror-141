# Photosynthetic
Photosynthetic is a python library that uses a unique clustering and distance algorithm to 
determine the perceptual color palette of an image. It offers a high degree of flexibility 
and configuration, allowing you to dial it in for post-processed images, illustrations, 
low-saturation, or product images!

A few examples of what you could do with this library:
* Create a fun, albeit useless, image host centered around color palettes like : https://photosynther.net
* Determine the primary color of product images for your eCommerce merchandising pipeline
* Have fun!
* Combine reference images into a brand guide or design system
* Automatically change themes based on profile images
* And probably at least a little but more

## Usage:
This library can be used one of two ways, you can import the package into your own project 
and use it as a library, or you can use it via the command line by passing in an image 
filepath as the first argument

### Command Line Usage
```bash
python main.py path/to/file.png
```

### Library Usage

Quickstart (Will extract a palette using sane and generic analysis defaults)
```python

from photosynthetic.Palette import Palette

p = Palette('images/test.png')
palette = p.extract()

print(palette)
# Returns :
# 
```