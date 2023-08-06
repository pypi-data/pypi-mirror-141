import math
import os

import numpy
from PIL import Image, ImageEnhance
from skimage import io

from skimage.data import astronaut
from skimage.color import rgb2gray, rgb2lab
from skimage.filters import sobel
from skimage.segmentation import felzenszwalb, slic, quickshift, watershed
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float
from skimage import exposure
import numpy as np
from skimage import data, io, segmentation, color
import numpy as np



class PaletteImage:

    def __init__(self, filepath, enhance=False, equalize=False):
        image = Image.open(filepath)
        # print(filepath)

        self.width = image.width
        self.height = image.height

        self.image = image

        img = io.imread(filepath)


        if equalize:
            img = self.equalize_histogram(img)

        self.scikit_image = img
        self.image_matrix = img_as_float(img)



        self.image_matrix = self.image_matrix[:, :, 0:3]

        if enhance:
            self.enhance()


        self.data = self.image.load()

    def get_superpixel_segments(self, segments=1000, algo='slic'):

        if algo == 'slic':
            segments = slic(self.image_matrix, n_segments=segments, compactness=10, max_iter=100, convert2lab=True, start_label=1)
        elif algo == 'quickshift':
            segments = quickshift(self.image_matrix)
        else:
            raise Exception("Please select a valid superpixel segments algorithm [quickshift, slic]")
        return segments

    def equalize_histogram(self, img):
        # Contrast stretching
        p2, p98 = np.percentile(img, (2, 98))
        img_rescale = exposure.rescale_intensity(img, in_range=(p2, p98))

        # Equalization
        img_eq = exposure.equalize_hist(img)

        # Adaptive Equalization
        img_adapteq = exposure.equalize_adapthist(img_eq, clip_limit=0.1)

        return img_adapteq

    def enhance(self):
        self.set_contrast()
        self.set_sharpness()
        self.set_brightness()

    def set_contrast(self, contrast=1.2):
        enhancer = ImageEnhance.Contrast(self.image)
        self.image = enhancer.enhance(contrast)

    def set_sharpness(self, sharpness=1.05):
        enhancer = ImageEnhance.Sharpness(self.image)
        self.image = enhancer.enhance(sharpness)

    def set_brightness(self, brightness=1.1):
        enhancer = ImageEnhance.Brightness(self.image)
        self.image = enhancer.enhance(brightness)

