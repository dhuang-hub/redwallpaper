from .RedWallpaperBufferBase import RedWallpaperBufferBase
from ..image import utils
from queue import Queue
import shutil
import requests

class ThumbnailBuffer(RedWallpaperBufferBase):
    def __init__(self, iterator, directory, tmp_dir=True, buffersize=80):
        super().__init__(iterator, directory, tmp_dir)
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
            fullsize_url, thumbnail_url = obj

            filename = None
            if thumbnail_url:
                try:
                    filename = utils.download_image(thumbnail_url, self.directory_buffer)
                except requests.exceptions.MissingSchema:
                    return
                except requests.exceptions.InvalidSchema:
                    return
                except requests.exceptions.InvalidURL:
                    return
                self.bufferQ.put((filename, fullsize_url))

            elif fullsize_url:
                try:
                    filename = utils.download_image(fullsize_url, self.directory_buffer)
                except requests.exceptions.MissingSchema:
                    return
                except requests.exceptions.InvalidSchema:
                    return
                except requests.exceptions.InvalidURL:
                    return
                utils.resize_img_file(filename)
                self.bufferQ.put((filename, fullsize_url))
        else:
            raise StopIteration