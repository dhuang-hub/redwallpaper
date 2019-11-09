# Automated Wallpaper

### Proposal
A tool that'll scrape for wallpapers from a high-quality image feed like [Reddit's Wallpapaper Subreddit](https://www.reddit.com/r/wallpapers/), and attempt to find popular up-voted wallpapers. It'll regularly change the computer's background at some predefined intervals.

Additional Features:
- GUI Interface: Runs quietly in the background
- Portable: Cross-platform for Windows and MacOS
- Popularity Filter: Scrapes wallpapers that meet a certain benchmark of popularity (upvotes)
- Color Filter: Allow users to predefine colors to serve as a search criteria
    - Allow for preset color palettes selection
    - Machine Learning: Allow users to predefine up to N colors to have the tool search by means of a 'color fingerprint'. This will be achieved by a k-means clustering technique on images, to derive the primary color 'fingerprint' for any image. An example of this [here](https://www.pyimagesearch.com/2014/05/26/opencv-python-k-means-color-clustering/).
    - Possible feature: Allow users to save favored color palettes
- Lightweight: Keep the minimal amount of images saved to the local drive. Allow users to save favorite wallpapers.

### Breakdown

To build this wallpaper tool, I'll be likely need to develop a few sets of tools deploying 3rd-party modules:
- OS Interactions: os, sys
- GUI:
    - Desktop: tkinter, PySide2, or PySimpleGUI
    - Web App: Flask or Django (Not familiar with web tools, so leaning towards a desktop GUI)
- WebScraping: requests and BeautifulSoup
- Machine Learning: sci-kit learn
