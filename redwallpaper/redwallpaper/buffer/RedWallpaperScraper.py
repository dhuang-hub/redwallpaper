from threading import Thread
from praw import Reddit
from praw.models.reddit.submission import Submission
from ..image import utils
import queue
import requests
import json


class RedWallpaperScraper:
    """
    Initializes and creates an instance of scraped submissions to the /r/subreddit.
    Stores submissions in the instance's 'wallpapers' attribute.
    """
    
    reddit_oath = {
        'client_id': 'pIxpnAoiGfwE-g',
        'client_secret': 'Ueccpv4dJegXUYbmAIdwxevxjDs',
        'user_agent': 'wallpapers'
    }
    
    
    imgur_oath = {
        'client_id': '29b27fc1363aa92',
        'client_secret': 'ef58b651b764dfb487809e64a2d62982e1a6392e'
    }
    
    
    imgur_headers = {
      'Authorization': f'Client-ID {imgur_oath["client_id"]}'
    }
    
    
    @staticmethod
    def get_imgur(url):
        """
        Queries the Imgur API with GET requests for images, given a valid Imgur url.
        This method is called to extract image urls from albums/galleries of images.
        """
        img_urls = []
        imgur_hash = url.strip('/').split('/')[-1].split('?')[0]
        
        # Unpredictable API endpoint
        api_album = f'https://api.imgur.com/3/album/{imgur_hash}/images'
        api_gallery = f'https://api.imgur.com/3/gallery/album/{imgur_hash}'
        api_kwargs = {
            'method':'GET',
            'url': None,
            'headers': RedWallpaperScraper.imgur_headers,
            'allow_redirects': False
        }
        
        for endpoint in [api_album, api_gallery]:
            api_kwargs['url'] = endpoint
            response = requests.request(**api_kwargs)
            if response.ok:
                # Imgur is very unpredictable!
                try:
                    img_urls += [image['link'] for image in json.loads(response.text)['data']]
                except TypeError:
                    img_urls += [image['link'] for image in json.loads(response.text)['data']['images']]
                break       
        return img_urls
    
    
    def __init__(self, sort='top', time_filter='week', limit=1000):
        """
        Initialize a wallpaper subreddit scraper instance with feed options.
        Stores wallpaper urls in a 'wallpaper' instance attribute'.
        Threaded extraction of urls allows for immediate access of wallpaper attribute
        while full extraction funs in the background.
        
        Sort options: 'top' (default), 'controversial', 'gilded', 'hot', 'new', 'rising'
        Time filters: 'week' (default), 'all', 'day', 'hour', 'month', 'year'
        Limit: Scrapes up to 1000 (max) submissions, 300 by default
        """
        self.wallpapers = queue.Queue()
        self.done = False
        self.end = False
        
        with Reddit(**self.reddit_oath) as R:
            r_wallpapers = R.subreddit('wallpapers')
            
            # sort_options = {'controversial', 'gilded', 'hot', 'new', 'rising', 'top'}
            # time_filter = {'all', 'day', 'hour', 'month', 'week', 'year'}
            
            if sort in {'controversial', 'top'}:
                r_wallpapers = getattr(r_wallpapers, sort)(limit=limit, time_filter=time_filter)
            else:
                r_wallpapers = getattr(r_wallpapers, sort)(limit=limit)

            Thread(target=self._get_all_wallpaper_url, args=(r_wallpapers,)).start()

                
    def __iter__(self):
        return self
    
    
    def __next__(self):
        try:
            return self.wallpapers.get(block=False)
        except queue.Empty:
            if self.done:
                raise StopIteration('Scraper: No more wallpapers')
            else:
                return self.wallpapers.get(block=True)
    
    
    def __len__(self):
        return self.wallpapers.qsize()

    
    def _get_wallpaper_url(self, r_submission):
        """
        Extract wallpaper url's from reddit submissions/posts. Appends to the instance's
        'wallpaper' attribute.
        """
        if isinstance(r_submission, Submission):
            if utils.is_img_ext(r_submission.url):
                self.wallpapers.put((r_submission.url, r_submission.thumbnail))
            elif 'imgur' in r_submission.url[:15]: # No need to search entire string
                for imgur_post in [(url, None) for url in self.get_imgur(r_submission.url)]:
                    self.wallpapers.put(imgur_post)
    
    
    def _get_all_wallpaper_url(self, r_wallpapers):
        """
        Runs a fully looped extraction of the r_wallpaper generator, calling helper function
        self._get_wallpaper_url
        """
        for r_submission in r_wallpapers:
            if not self.end:
                self._get_wallpaper_url(r_submission)
            else:
                raise StopIteration
        self.done = True

    
    def exit(self):
        self.end = True


    @property
    def empty(self):
        return self.wallpapers.empty()