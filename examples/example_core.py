#!/usr/bin/env python
# -*- coding: utf-8 -*-
from numba import jit
import numpy as np
from examples.helpers import show_image, tic, toc
from pyradar.core.sar import create_dataset_from_path
from pyradar.core.sar import get_band_from_dataset
from pyradar.core.sar import get_geoinfo
from pyradar.core.sar import read_image_from_band
from pyradar.core.sar import save_image
from pyradar.core.equalizers import equalization_using_histogram, naive_equalize_image


def eq(image):
    # equalize img to 0:255
    image_eq = equalization_using_histogram(image)
    # save img in current directory
    show_image(image_eq, 'Equalized image via Hist')


def naive_eq(image):
    # get actual range
    input_range = image.min(), image.max()
    # set new range
    output_range = 0, 255
    # equalize image
    image_eq = naive_equalize_image(image, input_range, output_range)
    # save image in current directory
    show_image(image_eq, 'Naive equalization')


def filters_eq(image):
    from pyradar.filters.frost import frost_filter
    from pyradar.filters.kuan import kuan_filter
    from pyradar.filters.lee import lee_filter
    from pyradar.filters.lee_enhanced import lee_enhanced_filter
    from pyradar.filters.median import median_filter
    from pyradar.filters.mean import mean_filter

    # filters parameters
    # window size
    winsize = 15
    # damping factor for frost
    k_value1 = 2.0
    # damping factor for lee enhanced
    k_value2 = 1.0
    # coefficient of variation of noise
    cu_value = 0.25
    # coefficient of variation for lee enhanced of noise
    cu_lee_enhanced = 0.523
    # max coefficient of variation for lee enhanced
    cmax_value = 1.73

    # frost filter
    tic('Frost')
    image_frost = frost_filter(image, damping_factor=k_value1, win_size=winsize)
    toc()
    show_image([(image, 'original'), (image_frost, 'Kuan') ])

    # kuan filter
    # tic('Kuan')
    # image_kuan = kuan_filter(image, win_size=winsize, cu=cu_value)
    # toc()
    # show_image([(image, 'original'), (image_kuan, 'Kuan') ])

    exit()
    # # lee filter
    tic('Lee')
    image_lee = lee_filter(image, win_size=winsize, cu=cu_value)
    toc()
    show_image([(image, 'original'), (image_lee, 'Lee') ])
    exit()
    # lee enhanced filter
    image_lee_enhanced = lee_enhanced_filter(image, win_size=winsize, k=k_value2,
                                             cu=cu_lee_enhanced, cmax=cmax_value)
    show_image(image_lee_enhanced, 'Enchanced Lee')

    # mean filter
    image_mean = mean_filter(image, win_size=winsize)
    show_image(image_mean, 'Mean')

    # median filter
    image_median = median_filter(image, win_size=winsize)
    show_image(image_median, 'Median')


def iso(image):
    # this should be placed at the top with all the imports
    from pyradar.classifiers.isodata import isodata_classification
    from pyradar.core.equalizers import equalization_using_histogram
    from pyradar.core.sar import save_image
    params = {"K": 15, "I": 100, "P": 2, "THETA_M": 10, "THETA_S": 0.1,
              "THETA_C": 2, "THETA_O": 0.01}

    # run Isodata
    class_image = isodata_classification(image, parameters=params)
    # equalize class image to 0:255
    class_image_eq = equalization_using_histogram(class_image)
    show_image(class_image_eq, 'isodata_classification')

def dud(image):
    show_image(image, 'isodata_classification')

def kmeans(image):
    from pyradar.classifiers.kmeans import kmeans_classification
    # number of clusters
    k= 4
    # max number of iterations
    iter_max = 1000
    # run K-Means
    class_image = kmeans_classification(image, k, iter_max)

    # equalize class image to 0:255
    class_image_eq = equalization_using_histogram(class_image)
    # save it
    show_image(class_image_eq, 'isodata_classification')


SAMPLES = [
    ('equalization_using_histogram', eq),
    ('naive_equalize_image', naive_eq),
    ('filters_eq', filters_eq),
    ('isodata', iso),
    ('kmeans', kmeans),
]

if __name__ == '__main__':
    IMAGE_PATH = "./img_sar/DAT_01.001"
    IMG_DEST_DIR = "."
    dataset = create_dataset_from_path(IMAGE_PATH)
    band = get_band_from_dataset(dataset)
    geoinfo = get_geoinfo(dataset, cast_to_int=True)
    xoff = geoinfo['xoff']
    yoff = geoinfo['yoff']
    win_xsize = 256
    win_ysize = 256
    image = read_image_from_band(band, xoff, yoff, win_xsize, win_ysize)
    keys = SAMPLES
    i = np.array(image).astype('float64')
    filters_eq(i)
    while(True):
        print('\n'.join(['%s). %s'%(id, k[0]) for id, k in enumerate(keys)]))
        print('-------------- \n')
        q = input('Select demo ID: ')
        keys[int(q)][1](image)