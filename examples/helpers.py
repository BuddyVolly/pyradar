import datetime

import matplotlib
import matplotlib.pyplot as plt
from PIL import Image
from skimage import color
import numpy as np
from object_recognition.keras_helpers import normalize_lab


def load_demo_image():
    im = color.rgb2lab(Image.open('../object_recognition/img/Patern_test.jpg'))/100.0
    return im[...,0]

MMT = 0
PROCESS = ''


def tic(process='Working'):
    global MMT, PROCESS
    PROCESS = process
    MMT = datetime.datetime.now()
    print('{:}... '.format(PROCESS))


def toc():
    global MMT, PROCESS
    t = datetime.datetime.now()
    interval = t - MMT
    MMT = t
    print('{:}: {:.2f} sec'.format(PROCESS, interval.total_seconds()))

def show_image(img, title=None):
    if isinstance(img, list):
        total = len(img)
        plt.title(title)
        per_row = np.floor(total**0.5)
        cols = np.ceil(total/per_row)
        for id, k in enumerate(img):
            plt.subplot(cols, per_row, 1+id)
            plt.title(k[1])

            plt.imshow(k[0], cmap='viridis', interpolation='nearest')
    else:
        plt.title(title)
        plt.imshow(img, cmap='viridis', interpolation='nearest')

    plt.show()

if __name__ == '__main__':
    i = load_demo_image()
    print(i.shape)
    show_image(i)
