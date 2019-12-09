import warnings
warnings.filterwarnings('ignore') 

from sklearn.cluster import KMeans
import cv2
import numpy as np


class RedWallpaperImage:
    """
    Class of objects that provides automated instantiation of image attributes
    such as color clustering, and image downsizing.
    """
    
    def __init__(self, input_array, colorspace='RGB', thumbnail=None, cluster=None):
        """
        Initialize Image instance, provided inputs of an image array, and optional
        image-downsizing to a thumbnail, and optional color clustering. Input of
        colorspace for reference, but is not checked for correctness. User needs
        to enforce correct default colorspace.
        Note: cv2 reads in images in 'BGR' colorspace by default
        """
        self.image = input_array
        self.colorspace = colorspace
        if self.colorspace != 'BGR':
            self.image = self.convert_color(self.image, 'BGR', self.colorspace)
        
        self.thumbnail = thumbnail
        self._set_thumbnail()
        
        self.cluster = cluster
        if self.cluster:
            self._set_color_cluster()
        else:
            self.rgb_cluster = None
            self.rgb_cluster_lab = None
            self.lab_cluster = None
        

    @classmethod
    def from_filepath(cls, filepath, colorspace='RGB', thumbnail=None, cluster=None):
        """
        Method to read in images directly from filepaths
        """
        input_array = cv2.imread(filepath)
        return cls(input_array, colorspace, thumbnail, cluster)
    
    
    @staticmethod
    def convert_color(img_array, color_in, color_out):
        """
        Static method for color conversions between the three color spaces
        of: BGR, RGB, and L*a*b.
        """
        shape = img_array.shape
        
        # For non-image arrays, of two dimension, e.g. self.rgb_cluster
        if len(shape) < 3:
            img_array = img_array.reshape((1,)+shape)
        img_array = img_array.astype('uint8')
        
        # RGB to BGR/L*a*b
        if color_in == 'RGB':
            if color_out == 'BGR':
                img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            elif color_out == 'LAB':
                img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2LAB)
        # BGR to RGB/L*a*b
        elif color_in == 'BGR':
            if color_out == 'RGB':
                img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
            elif color_out == 'LAB':
                img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2LAB)
        # L*a*b to RGB/BGR
        elif color_in == 'LAB':
            if color_out == 'RGB':
                img_array = cv2.cvtColor(img_array, cv2.COLOR_LAB2RGB)
            elif color_out == 'BGR':
                img_array = cv2.cvtColor(img_array, cv2.COLOR_LAB2BGR)
        
        if len(shape) < 3:
            img_array = img_array.reshape(shape)
            
        return img_array
    
    
    @property
    def shape(self):
        """
        Get Image array shape.
        """
        return self.image.shape
    
    
    def resize(self, width=140, height=None, inter=cv2.INTER_AREA):
        """
        Initialize the dimensions of the image to be resized and
        grab the self size. Default settings will downsize an image into
        a thumbnail.
        Note: Borrowed function, credit goes to github.com/jrosebr1/imutils
        """ 
        img = self.image
        dim = None
        h, w = img.shape[:2]

        # original image
        if width is None and height is None:
            return img
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

        # resize the self
        resized = cv2.resize(img, dim, interpolation=inter)

        # return the resized self
        return resized
    
    
    def _set_thumbnail(self):
        """
        Sets/enforces the Image thumbnail option during instantiation. If
        self.thumbnail is None, the attribute will be set by a boolean determination
        on whether or not the Image is the size of a thumnail. If self.thumbnail is
        True, the thumbnail option will be enforced and large Images will be downsized.
        """
        if self.thumbnail is None:
            self.thumbnail = self.image.size <= (170 * 170)
        elif self.thumbnail and self.image.size > (170 * 170):
            self.image = self.resize()
    

    @staticmethod
    def color_cluster(img_array, k=3):
        """
        A static method to cluster colors of img_arrays (height x width x colors).
        The number of clusters calculated depends is determined by input k.
        Returns a (k x 3) dimensional ndarray.
        """
        # Flatten image array
        img_array = img_array.reshape((img_array.shape[0] * img_array.shape[1], 3))
        clt = KMeans(n_clusters = k)
        clt.fit(img_array)
        return clt.cluster_centers_
    

    def _set_color_cluster(self):
        """
        Sets the Image's attributes of color clusters, clustered by colors in 'RGB'
        the colorspace and by colors in the 'L*a*b' color space.
        """
        k = self.cluster
        color_in = self.colorspace
        
        rgb = self.convert_color(self.image, color_in, 'RGB')
        self.rgb_cluster = self.color_cluster(rgb, k)
        self.rgb_cluster_lab = self.convert_color(self.rgb_cluster, 'RGB', 'LAB')

        lab = self.convert_color(self.image, color_in, 'LAB')
        self.lab_cluster = self.color_cluster(lab, k)


def main():
    RedWallpaperApp.RedWallpaperApp()

if __name__ == '__main__':
    main()