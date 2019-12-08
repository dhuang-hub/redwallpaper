from queue import Queue
from .RedWallpaperBufferBase import RedWallpaperBufferBase
from ..image import utils

class FullsizeBuffer(RedWallpaperBufferBase):
    def __init__(self, iterator, directory, tmp_dir=False, buffersize=2):
        super().__init__(iterator, directory, tmp_dir)
        
        #self.wallpapers = []
        #self.current = None
        
        # For maintaining a set of wallpapers to save -- Not delete
        self.keep = set()
        
        self.bufferQ = Queue(maxsize=buffersize)
        self.buffer_all()
    
    
    def __del__(self):
        pass
    
    
    
    def buffer(self, obj):
        score, fullsize_url = obj
        
        filename = None
        filename = utils.download_image(fullsize_url, self.directory)
        #self.wallpapers.append(filename)
        #self.current = filename
        self.bufferQ.put((filename, score))
