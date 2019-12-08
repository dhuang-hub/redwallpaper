from .RedWallpaperBufferBase import RedWallpaperBufferBase
from ..image.RedWallpaperImage import RedWallpaperImage
from ..image import utils
from queue import PriorityQueue

class ScoredBuffer(RedWallpaperBufferBase):
    def __init__(self, iterator, directory, master_rgb_lab, master_lab, cluster=None,
                 tmp_dir=False, score_threshold=100):
        super().__init__(iterator, directory, tmp_dir)
        self.master_rgb_lab = master_rgb_lab
        self.master_lab = master_lab
        self.cluster = cluster
        self._score_threshold = score_threshold
        self.bufferQ = PriorityQueue()
        self.buffer_all()


    @property
    def score_threshold(self):
        return self._score_threshold
    
    
    @score_threshold.setter
    def score_threshold(self, value):
        self._score_threshold = value
    
    
    def __del__(self):
        pass
    
    
    def buffer(self, obj):
        k = self.cluster
        thumbnail_file, fullsize_url = obj
        thumbnail = RedWallpaperImage.from_filepath(thumbnail_file, cluster=k)
        # pylint doesn't understand decorators!
        # pylint: disable=E1121
        rgb_lab_score = utils.delta_e_94(thumbnail.rgb_cluster_lab, self.master_rgb_lab)
        lab_score = utils.delta_e_94(thumbnail.lab_cluster, self.master_lab)
        # pylint: enable=E1121

        score = rgb_lab_score + lab_score

        if score <= self.score_threshold:
            self.bufferQ.put((score, fullsize_url))
        
        
    