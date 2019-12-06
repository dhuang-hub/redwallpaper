from itertools import permutations
from sklearn.cluster import KMeans
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


def min_delta_e(func):
    def delta_e_func(*args):
        colors1, colors2 = args
        min_delta_e = float('inf')
        for colors1_ in permutations(colors1):
            min_delta_e = min(sum(map(func, zip(colors1_, colors2))), min_delta_e)
        return min_delta_e
    return delta_e_func


def delta_e_94(colors):
    Lab1, Lab2 = colors
    
    # Constants
    KL = 2
    K1 = 0.045
    K2 = 0.015
    
    # Variables
    L1, a1, b1 = Lab1.astype('int')
    L2, a2, b2 = Lab2.astype('int')
    
    C1 = (a1**2 + b1**2) ** (0.5)
    C2 = (a2**2 + b2**2) ** (0.5)
    
    delta_L = L1 - L2
    delta_a = a1 - a2
    delta_b = b1 - b2
    delta_C = C1 - C2
    delta_H = (delta_a**2 + delta_b**2 - delta_C**2) ** (0.5)
    
    SL = KL
    SC = 1 + K1*C1
    SH = 1 + K2*C1
    
    # Calculate
    return ((delta_L / SL)**2 + (delta_C / SC)**2 + (delta_H / SH)**2) ** (0.5)


def read_image(filepath, color=None):
    """
    Function for reading in an image
    """

    image = cv2.imread(filepath)
    
    if color == 'RGB':
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    elif color == 'LAB':
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    else:
        color = 'BGR'
    
    image.color = color
    
    return image


def convert_color(image, in_color, out_color):
    """
    Function for converting an image's color space
    """

    image = image.astype('uint8').reshape((1,3,3))
    if in_color == 'RGB':
        if out_color == 'BGR':
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        elif out_color == 'LAB':
            image = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)

    elif in_color == 'BGR':
        if out_color == 'RGB':
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        elif out_color == 'LAB':
            image = cv2.cv2Color(image, cv2.COLOR_BGR2LAB)

    elif in_color == 'LAB':
        if out_color == 'RGB':
            image = cv2.cvtColor(image, cv2.COLOR_LAB2RGB)
        elif out_color == 'BGR':
            image = cv2.cv2Color(image, cv2.COLOR_LAB2BGR)
    return image.reshape((3,3))