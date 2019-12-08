from abc import ABC, abstractmethod
from threading import Thread
from time import sleep
import os
import tempfile
import queue

class RedWallpaperBufferBase(ABC):
    
    def __init__(self, iterator, directory, tmp_dir=True):
        self.iterator = iterator
        self.done = False

        self.directory = self.init_dir(directory)
        if tmp_dir:
            self.directory_buffer = self.init_dir(directory, tmp=tmp_dir)

        self.bufferQ = None

    
    def __len__(self):
        return self.bufferQ.qsize()
        
        
    def __iter__(self):
        return self

    
    def __next__(self):
        try:
            return self.bufferQ.get(block=False)
        except queue.Empty:
            if self.done:
                raise StopIteration
            else:
                return self.bufferQ.get(block=True)

    
    @abstractmethod
    def __del__(self):
        pass
        
        
    def init_dir(self, directory, tmp=False):
        """
        Initializes a directory, if it doesn't exist, it'll make the directory.
        If tmp=True, it'll create a temporary directory nested within the input
        directory.
        """
        if not os.path.exists(directory):
            os.mkdir(directory)
        if tmp:
            tmpdirectory = tempfile.mkdtemp(dir=directory)
            return tmpdirectory
        return directory
        
        
    @abstractmethod
    def buffer(self, obj):
        # Buffer from the iterator and do something
        # Add to bufferQ
        pass


    def buffer_all(self):
        Thread(target=self._buffer_all).start()

        
    def _buffer_all(self):
        while not (self.iterator.done and self.iterator.empty):
            try:
                obj = next(self.iterator)
                self.buffer(obj)
            except StopIteration:
                sleep(1)
        self.done = True
    
    @property
    def empty(self):
        return self.bufferQ.empty()