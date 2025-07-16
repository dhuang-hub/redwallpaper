from .buffer.RedWallpaperScraper import RedWallpaperScraper
from .buffer.ThumbnailBuffer import ThumbnailBuffer
from .buffer.ScoredBuffer import ScoredBuffer
from .buffer.FullsizeBuffer import FullsizeBuffer
from .image.RedWallpaperImage import RedWallpaperImage
from .image import utils
from .set_wallpaper import set_wallpaper
import logging
import os
import shutil
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RedWallpaperApp:
    """
    This is the Command-Line interface of the entire project.
    With this class, it'll serve as the intializer and coordinator of information between
    the buffer and image objects.
    """

    def __init__(self):
        logger.info('Welcome to Red Wallpaper! Time to find a new desktop wallpaper from /r/wallpapers.')
        
        self.master_file = None
        self.master_image = None
        self.k = 0
        self.pick_color_palette()
        
        self.listing = None
        self.pick_listing()
        
        self.time_filter = None
        self.pick_time_filter()
        
        self.directory = None
        self.pick_directory()
        self.save_directory = os.path.join(self.directory, 'redwallpaper_saved')
        if not os.path.isdir(self.save_directory):
            os.mkdir(self.save_directory)
        
        self.initialize()
        self.run()
        self.end()
        
        

    def pick_master_image(self):
        """
        Console UI for selecting a valid image on the local drive for color palette
        selection.
        """
        console = 'Please select an image from which to extract a color palette: '
        master_file = None
        master_file = input(console)
        while not (os.path.exists(master_file) and utils.is_img_ext(master_file)):
            logger.warning('Invalid image file, must be a valid .jpg or .png.')
            master_file = input(console)
        self.master_file = master_file
        
    
    def pick_k_cluster(self):
        """
        Console UI for selecting the number of colors to extract from an image by
        means of KMeans clustering.
        """
        console = 'Please select the number of colors to extract for a color palette: '
        k = None
        k = input(console)
        while not (k.isdigit() and 0 < int(k) <= 5):
            logger.warning('Invalid number, must be an integer 1 through 5.')
            k = input(console)
        self.k = int(k)
        
        
    def pick_color_palette(self):
        """
        Console UI for picking a color palette to seek by processing a local image on file,
        and by selecting the number of colors to extract from the selected image.
        """
        console = 'Proceed with this color palette? (Yes/No): '
        while True:
            self.pick_master_image()
            self.pick_k_cluster()
            self.master_image = RedWallpaperImage.from_filepath(self.master_file,
                                                                thumbnail=True,
                                                                cluster=self.k)
            utils.color_cluster_display(self.master_image)
            decision = input(console).lower()
            
            while decision not in {'y', 'n', 'yes', 'no'}:
                logger.warning('Invalid option!')
                decision = input(console).lower()
            plt.close('all')
            if decision[0] == 'y':
                break
    
    
    def pick_listing(self):
        """
        Console UI for selecting a valid listing, or sort option of /r/wallpapers.
        """
        listing_options = {
            't': 'top',
            'c': 'controversial',
            'g': 'gilded',
            'h': 'hot',
            'n': 'new',
            'r': 'rising'
        }
        console = "Please select a listing: 'top', 'controversial', 'gilded', 'hot', 'new', 'rising': "
        listing = None
        listing = input(console).lower()
        while listing not in listing_options.keys() \
            and listing not in listing_options.values():
            logger.warning('Invalid selection! Try selecting with just the first character.')
            listing = input(console).lower()
        self.listing = listing_options[listing[0]]
        
    
    def pick_time_filter(self):
        """
        Console UI for selecting a valid time filter based on the listing selected by the user.
        Not all listings will allow for a time filter, only the 'Top' and 'Controversial'
        listings allow for a time filter.
        """
        if self.listing in {'controversial', 'top'}:
            time_options = {
                'a': 'all',
                'd': 'day',
                'h': 'hour',
                'm': 'month',
                'w': 'week',
                'y': 'year'
            }
            console = "Please select a time filter: 'all', 'day', 'hour', 'month', 'week', 'year': "
            time_filter = None
            time_filter = input(console).lower()
            while time_filter not in time_options.keys() \
                and time_filter not in time_options.values():
                logger.warning('Invalid selection! Try selecting with just the first character.')
                time_filter = input(console).lower()
            self.time_filter = time_options[time_filter[0]]
            
            
    def pick_directory(self):
        """
        Console UI for selecting a valid working directory.
        """
        console = ('''Please provide a working directory for storing wallpaper images: ''')
        
        while True:
            directory = input(console)
            if not os.path.isdir(directory):
                logger.warning('Invalid directory!')
                continue
            correct = None
            correct = input(f"Is \'{os.path.abspath(directory)}\' correct? (Yes/No): ").lower()
            while correct not in {'y', 'n', 'yes', 'no'}:
                logger.warning('Invalid option!')
                correct = input(f"Is \'{directory}\' correct? (Yes/No): ").lower()
            if correct[0] == 'y':
                break
                
        self.directory = directory       
        
        
    def initialize(self):
        """
        Initializes and this in turn automatically starts the waterfall of buffers.
        Scrape the url > Get the thumbnail > Score the color > Download good ones.
        """
        directory = self.directory
        self.scraper = RedWallpaperScraper(self.listing, self.time_filter)
        self.thumb_buff = ThumbnailBuffer(self.scraper, directory)
        self.score_buff = ScoredBuffer(self.thumb_buff,
                                       directory,
                                       self.master_image.rgb_cluster_lab,
                                       self.master_image.lab_cluster,
                                       self.k)
        self.full_buff = FullsizeBuffer(self.score_buff, directory)

    
    def run(self):
        """
        Runs the setting and saving of wallpapers with user input options of 
        (N)ext, (S)ave, and (E)xit.
        """
        console = (
'''
Wallpapers available to set!
Input options:
    (N)ext: Set the next wallpaper
    (S)ave: Flag to keep wallpaper and prevent deletion during clean-up
            Saved wallpapers can be found in a 'redwallpaper_saved'
            folder created within the directory you selected.
    (E)xit: End and clean-up
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
''')
        # Initialize wallpaper file var
        wallpaper = None
        # User input var
        user = None
        while True:
            user = input(console).lower()
            
            if user not in {'n', 's', 'e'}:
                logger.warning('Invalid option!')
                continue
            
            # Next wallpaper
            if user == 'n':
                
                try:
                    # pylint: disable=unused-variable
                    wallpaper, score = next(self.full_buff)
                    # pylint: enable=unused-variable
                # End if no more wallpapers
                except StopIteration:
                    break
                set_wallpaper(wallpaper)
            
            # Save wallpaper
            if user == 's':
                file = wallpaper.split('/')[-1]
                shutil.copy(wallpaper, os.path.join(self.save_directory, file))
                
            # End
            if user == 'e':
                break
                
                
    def end(self):
        """
        Exit all the threaded buffers by raising the buffers' end flag which will
        raise a StopIteration exception. Finally, remove buffers that have buffer
        directories.
        """
        for buff in [self.scraper, self.thumb_buff, self.score_buff, self.full_buff]:
            # Send the exit flag, raises the 'end' flag/attr of each buffer
            try:
                buff.exit()
            # Expecting this to trigger
            # Stops the threads!
            except StopIteration:
                pass
            # Finally clean-up
            finally:
                if getattr(buff, 'directory_buffer', None):
                    shutil.rmtree(buff.directory_buffer)
