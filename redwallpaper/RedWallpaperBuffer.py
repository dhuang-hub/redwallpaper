import os
import shutil
import tempfile
#from threading import Thread
from . import utils
from queue import Queue

class RedWallpaperBuffer:
    def __init__(self, redwallpaperscraper, directory): #, buffersize=10):
        self.redwallpaperscraper = redwallpaperscraper

        self.directory = self.init_dir(directory)
        self.directory_buffer = self.init_dir(directory, tmp=True)
        
        #self.bufferQ = Queue(maxsize=)
        self.bufferQ = Queue()
        #self.buffersize = buffersize
        self._buffercount = 0
#         self.buffer()
    
    
    def init_dir(self, directory, tmp=False):
        """
        Initializes a directory, if it doesn't exist, it'll make the directory.
        If tmp=True, it'll create a temporary directory nested within the input directory.
        """
        if not os.path.exists(directory):
            os.mkdir(directory)
        if tmp:
            tmpdirectory = tempfile.mkdtemp(dir=directory)
            return tmpdirectory
        return directory
    
    
    def buffer(self):
        try:
            fullsize, thumbnail = next(self.redwallpaperscraper)
        except StopIteration:
            raise StopIteration
        filename = None
        if thumbnail:
            filename = utils.download_image(thumbnail, self.directory_buffer)
        else:
            filename = utils.download_image(fullsize, self.directory_buffer)
            utils.resize_img_file(filename)
        self.bufferQ.put((filename, fullsize))
        self._buffercount += 1
        
        
    def __iter__(self):
        return self
    
    
    def __next__(self):
        if not self.bufferQ.empty():
            self._buffercount -= 1
            return self.bufferQ.get()
        # self.__del__()
        raise StopIteration
            
            
#    def __del__(self):
#        shutil.rmtree(self.directory_buffer)