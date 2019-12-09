from redwallpaper.buffer.RedWallpaperScraper import RedWallpaperScraper
from redwallpaper.buffer.ThumbnailBuffer import ThumbnailBuffer
from redwallpaper.buffer.ScoredBuffer import ScoredBuffer
from redwallpaper.buffer.FullsizeBuffer import FullsizeBuffer
from redwallpaper.image.RedWallpaperImage import RedWallpaperImage
from redwallpaper.image import utils
from redwallpaper.set_wallpaper import set_wallpaper

from time import sleep
import shutil
import numpy as np
import os


# NOT SURE WHY I CANT GET THIS TO WORK???
# Works fine in my notebook
# But I can't figure out why this won't recognize this local directory image???
test_image = 'master_image.jpg'

# Tested and troubleshooted a bunch of times.
# Unfortunately ran out of time here
# test_image = ('/'.join(os.path.os.path.abspath('.').split('/'))+'/'+ test_image)



def scraper_test():
    scraper = RedWallpaperScraper('top', 'day', 10)
    # Starts out empty
    assert scraper.empty
    # Not yet done
    assert not scraper.done
    
    # Allow it time to scrape
    sleep(3)
    # Check it has buffered
    assert not scraper.empty
    # Empty the buffer
    while not scraper.empty:
        next(scraper)
    # Assert empty buffer
    assert scraper.empty
    # Assert empty flag
    assert scraper.done
    
    # Check for an end flag
    scraper.exit()
    assert scraper.end

scraper_test()

def image_test():
    image = RedWallpaperImage.from_filepath(test_image, thumbnail=True, cluster=3)
    
    # Check that it has an image
    assert hasattr(image, 'image')
    # Check that it is correctly read-in
    assert isinstance(getattr(image, 'image'), np.ndarray)
    # Check for the correct default colorspace conversion
    # Implies a correct color conversion
    # cv2 defaults to 'BGR'
    assert getattr(image, 'colorspace') == 'RGB'
    # Check for a correct downsizing
    assert image.image.size <= (170 * 170 * 3)
    # Check for a correct clustering
    assert getattr(image, 'cluster', None) > 0
    assert getattr(image, 'rgb_cluster', None) is not None
    assert getattr(image, 'lab_cluster', None) is not None
    assert getattr(image, 'rgb_cluster_lab', None) is not None
    
image_test()

def utils_test():
    a = np.asarray([[0,1,2], [3,4,5], [6,7,8]])
    b = np.asarray([[3,4,5], [0,1,2], [6,7,8]])
    # Check for correct minimum distance
    assert utils.delta_e_94(a, b) == 0
    
    # Check for correct image file functions
    assert utils.is_img_ext(('.' + utils.get_file_ext(test_image)))
    
    # Check for correct in-place resizing
    # Copy large image, resize, assert, delete
    test_image2 = shutil.copy(test_image, 'master_image2.jpg')
    utils.resize_img_file(test_image2)
    x, y, z = RedWallpaperImage.from_filepath(test_image2, thumbnail=False).image.shape
    assert x * y <= (170 * 170)
    os.remove(test_image2)
    
utils_test()

def buffer_test():
    image = RedWallpaperImage.from_filepath(test_image, thumbnail=True, cluster=3)
    scraper = RedWallpaperScraper('top', 'day', 10)
    thumb_buff = ThumbnailBuffer(scraper, 'test')
    score_buff = ScoredBuffer(thumb_buff, 'test',
                              image.rgb_cluster_lab,
                              image.lab_cluster,
                              image.cluster,
                              score_threshold=0
                             )
    full_buff = FullsizeBuffer(score_buff, 'test')
    
    
    for buff in [scraper, thumb_buff, score_buff, full_buff]:
        # Check for completion flags
        if buff.done:
            # Check for empty flags
            assert buff.empty
        
    assert getattr(thumb_buff, 'directory_buffer', None) is not None
    assert getattr(full_buff, 'directory_buffer', None) is not None
    
    sleep(3)
    
    # Check clean-up
    for buff in [scraper, thumb_buff, score_buff, full_buff]:
        # Send the exit flag, raises the 'end' flag/attr of each buffer
        try:
            buff.exit()
        # Expecting this to trigger
        # Stops the threads!
        except StopIteration:
            pass
        # Finally clean-up
        finally:
            # Check that the end flag is true
            assert buff.end is True
            if getattr(buff, 'directory_buffer', None):
                shutil.rmtree(buff.directory_buffer)
    
    shutil.rmtree('test')
buffer_test()