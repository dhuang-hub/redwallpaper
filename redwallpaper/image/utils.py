from itertools import permutations
from sklearn.cluster import KMeans
from math import sqrt
import os
import tempfile
import requests
import cv2


def is_img_ext(file):
    """
    Determines existence of a .jpg or .png file extension from a url string
    """
    return file[-4:] in {'.jpg','.png'}


def get_file_ext(file):
    """
    Given a file, returns the file extension
    """
    return f".{file.split('.')[-1]}"


def download_image(url, directory, delete=False):
    """
    Given an image url and file directory, the image is saved to the
    directory. Returns the file's directory path.
    """
    file_ext = get_file_ext(url)
    with tempfile.NamedTemporaryFile('wb', suffix=file_ext, dir=directory,
                                     delete=delete) as tmp:
        r = requests.get(url, stream=True)
        if r.ok:
            tmp.write(r.content)
        return os.path.join(directory, tmp.name.split('/')[-1])


def min_delta_e(func):
    def delta_e_func(*args):
        colors1, colors2 = args
        min_delta = float('inf')
        for colors1_ in permutations(colors1):
            min_delta = min(sum(map(func, zip(colors1_, colors2))), min_delta)
        return min_delta
    return delta_e_func

@min_delta_e
def delta_e_94(colors):
    Lab1, Lab2 = colors
    
    # Constants
    KL = 1.5
    K1 = 0.045
    K2 = 0.015
    
    # Variables
    L1, a1, b1 = Lab1.tolist()
    L2, a2, b2 = Lab2.tolist()
    
    C1 = sqrt(a1**2 + b1**2)
    C2 = sqrt(a2**2 + b2**2)
    
    delta_L = L1 - L2
    delta_a = a1 - a2
    delta_b = b1 - b2
    delta_C = C1 - C2
    delta_H = sqrt(max(delta_a**2 + delta_b**2 - delta_C**2, 0))
    
    SL = KL
    SC = 1 + K1*C1
    SH = 1 + K2*C1
    
    # Calculate
    return sqrt((delta_L / SL)**2 + (delta_C / SC)**2 + (delta_H / SH)**2)


def resize(image, width=140, height=None, inter=cv2.INTER_AREA):
    # Borrowed function, credit goes to github.com/jrosebr1/imutils
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # original image
    if width is None and height is None:
        return image
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
    return resized


def resize_img_file(file):
    img = cv2.imread(file)
    img = resize(img)
    cv2.imwrite(file, img)