from .RedWallpaperBufferBase import RedWallpaperBufferBase
from ..image import utils
from queue import Queue
import shutil

class ThumbnailBuffer(RedWallpaperBufferBase):
    def __init__(self, iterator, directory, tmp_dir=True, buffersize=80):
        super().__init__(iterator, directory, tmp_dir)
        self.bufferQ = Queue(maxsize=buffersize)
        self.buffer_all()
        
        
    def __del__(self):
        shutil.rmtree(self.directory_buffer)
    
    
    def buffer(self, obj):
        fullsize_url, thumbnail_url = obj

        filename = None
        if thumbnail_url:
            filename = utils.download_image(thumbnail_url, self.directory_buffer)
        else:
            filename = utils.download_image(fullsize_url, self.directory_buffer)
            utils.resize_img_file(filename)
        self.bufferQ.put((filename, fullsize_url))