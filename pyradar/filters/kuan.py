#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2012 - 2013
# Matías Herranz <matiasherranz@gmail.com>
# Joaquín Tita <joaquintita@gmail.com>
#
# https://github.com/PyRadar/pyradar
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library. If not, see <http://www.gnu.org/licenses/>.


import numpy as np
from numba import jit, float64, int16
from scipy.stats import variation

from .utils import assert_window_size
from .utils import assert_indices_in_range

COEF_VAR_DEFAULT = 0.01
CU_DEFAULT = 0.25


# @jit(cache=True, nopython= True)
def weighting(window, cu=CU_DEFAULT):
    """
    Computes the weighthing function for Kuan filter using cu as the noise
    coefficient.
    """
    two_cu = cu * cu

    ci = variation(window, None)
    two_ci = ci * ci

    if not two_ci:  # dirty patch to avoid zero division
        two_ci = COEF_VAR_DEFAULT

    divisor = 1.0 + two_cu

    if not divisor:
        divisor = 0.0001

    if cu > ci:
        w_t = 0.0
    else:
        w_t = (1.0 - (two_cu / two_ci)) / divisor

    return w_t


@jit(float64[:,:](float64[:,:], int16, float64), cache=True, nopython= True)
def kuan_filter(img, win_size=3, cu=CU_DEFAULT):
    """
    Apply kuan to a numpy matrix containing the image, with a window of
    win_size x win_size.
    """

    # assert_window_size(win_size)

    # we process the entire img as float64 to avoid type overflow error
    img_filtered = np.zeros_like(img)
    two_cu = cu * cu
    divisor = 1.0 + two_cu
    if not divisor:
        divisor = 0.0001

    N, M = img.shape
    win_offset = win_size / 2

    for i in range(0, N):
        xleft = i - win_offset
        xright = i + win_offset

        if xleft < 0:
            xleft = 0
        if xright >= N:
            xright = N

        for j in range(0, M):
            yup = j - win_offset
            ydown = j + win_offset
            if yup < 0:
                yup = 0
            if ydown >= M:
                ydown = M
            pix_value = img[i, j]
            window = img[xleft:xright, yup:ydown]
            window_mean = window.mean()
            window_std = window.std()
            ci = window_std / window_mean
            two_ci = ci * ci

            if two_ci == 0:  # dirty patch to avoid zero division
                two_ci = COEF_VAR_DEFAULT

            if cu > ci:
                w_t = 0.0
            else:
                w_t = (1.0 - (two_cu / two_ci)) / divisor

            new_pix_value = (pix_value * w_t) + (window_mean * (1.0 - w_t))

            img_filtered[i, j] = round(new_pix_value)

    return img_filtered
