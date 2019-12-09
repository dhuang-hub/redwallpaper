from queue import Queue
from .RedWallpaperBufferBase import RedWallpaperBufferBase
from ..image import utils
import shutil

class FullsizeBuffer(RedWallpaperBufferBase):
    def __init__(self, iterator, directory, tmp_dir=True, buffersize=2):
        super().__init__(iterator, directory, tmp_dir)
        
        self.wallpapers = []
              
        self.bufferQ = Queue(maxsize=buffersize)
        self.buffer_all()
    
    
    def __del__(self):
        try:
            self.exit()
        except StopIteration:
            raise StopIteration
        finally:
            shutil.rmtree(self.directory_buffer)
    
    
    def buffer(self, obj):
        if not self.end:
            score, fullsize_url = obj
            
            filename = None
            filename = utils.download_image(fullsize_url, self.directory_buffer)
            self.wallpapers.append(filename)
            self.bufferQ.put((filename, score))
        else:
            raise StopIteration