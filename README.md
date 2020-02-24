# redwallpaper

Welcome to redwallpaper!

This is a python package that is intended to serve as a fun little
tool to provide an interesting feed and take on desktop wallpapers.

Provided an image, this command-line tool will run and decompose intended
into a color palette of 1 to 5 colors, using K-Means clustering. Its
accuracy questionable when tries to work on images of high color ranges
but it works adequately well. With color palettes, this tool will seek
out similar images with similar color palettes. E.g. a blue palette
will tend to return a bunch of (mostly) blue desktop wallpapers.

This tool was intended to be implemented as a GUI, but pressed for time,
I settled to implement it as a command-line tool. Unfortunately, I don'take
think I correctly implemented this package hierarchy. So the relative imports,
I believe may end up upbraiding a correct and flawless run.

However, I insist that this tool does work.

Built with a pipeline of buffers.
It first must crawl through the Reddit API and pull out up to the max of 1k
posts.
Then it downloads thumbnails, and if thumbnails aren't available, it'll
create thumbnails.
With thumbnails, redwallpaper proceeds to cluster the colors and score it
against the selected color palette.
From the scored images, the last pipeline is the full-size download.

A pipeline of 4 buffers.

These are all threaded buffers, to allow for a seemless, and interrupted 
user experience. The user will be able to iterate through wallpapers,
save wallpapers, and end the app prematurely should they desire.

I've used a lot of modules:
    - os
    - praw (reddit api wrapper)
    - requests
    - matplotlib
    - shutil
    - sklearn
    - numpy
    - math
    - tempfile
    - queue
    - platform
    - appscript
    - ctypes
    - cv2

To run, please run the python file at the top-directory, 'main.py'
The rest of the app will direct the user with clear instructions.
Fail-safe measures are implemented to ensure users don't input invalid
inputs.

I've implemented this to be portable for Windows, Linux, and Darwin (OS),
however, I've only extensively tested this for Darwin (OS) systems.
