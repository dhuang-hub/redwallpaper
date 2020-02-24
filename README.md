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
I believe may end up becoming the ruin of a correct and flawless run.

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



Details on Implementation:

I hope to flush out in greater details the inner workings of this project
here in this readme.

My project is a desktop wallpaper search that searches for wallpapers
from the reddit.com/r/wallpapers feed of community-submitted
wallpapers. There are many different sites with high-quality images,
however, I settled on reddit because I felt that it would allow for
a broader and more interesting range of images. To access Reddit,
I queried from their API. In order to do this, I deployed the 'praw'
module, which is the 'official' Python wrapper created for the API.
My reasoning behind doing this was because 'praw' would be able to
automatically handle the query request limits, where it'll pause
large chunks of queries if it detects that the query it pushing near
the API's limits. This is all happens in a buffer.RedwallpaperScraper
instance.

My project is developed to allow users to serach by color. This was an 
interesting and wonderful learning experience on image processing. This
was a lot trickier than I had initially anticipated. I derived inspiration
from here:
https://www.pyimagesearch.com/2014/05/26/opencv-python-k-means-color-clustering/.
I wanted to allow a user to create a color palette, or color fingerprint,
to serve as a unique identifiable image attribute with which 'redwallpaper'
will search with, score with, and ultimately find wallpapers with.
To process these images, I used 'OpenCV's python module, 'cv2'. Images are
processed into 'numpy' arrays. With these image arrays, I clustered images using
'sklearn' for KMeans clustering. Clustering turned out to be very slow
on large images of high-quality. Fortunately, with 'praw', I was able to
extract image thumbnails. With extensive testing, the thumbnails were quick
to cluster, and provided color centroids that were nearly just as good as the
high-quality image KMeans. In cases where thumbnails didn't exist, I'd
download the high-quality image, and downsize it locally. This all happens in
a buffer.ThumbnailBuffer instance.

Scoring color distance, or color delta, is tricky. I learned a lot about color
spaces. Color in the 'RGB' color space that we're familiar with, is a
non-Euclidean color space. This meant that taking the square root of squared
differences between two Red's, two Green's, and two Blue's respective of two
colors, wouldn't derive a consistent delta between hues and lightnes/darkness
for the human eye. I had to switch to use the L*a*b colorspace, and used a
color delta formula named 'Delta-E 94' that calculates the color distance/delta
between two L*a*b colors. Since a user can cluster anywhere between 1 and 5
colors from an image (redwallpaper enforced), there must be a Cartesian
product and comparison between two sets of colors, as redwallpaper seeks to
find the minimum distance/delta between the two sets of colors. I achieved this
by permuting one set of colors, and zipping it together with the second set.
A resource I found very helpful: http://zschuessler.github.io/DeltaE/learn/.
I had to play and monkey around with a few different manners of scoring to
derive results that were passable. Even with the Delta-E 94, I don't think the
results are as great as I had hoped. There are more complex color formulas
in existence, so I developed with the hopes of allowing for an easy swap of
scoring functions. This was achieved with creating the minimum search of
Cartesian products of two sets of colors as a decorator function. See in 
image.utils. All the scoring takes place in a buffer.ScoredBuffer instance.

Finally, if an image's thumbnail adequately scores close enough to the user's
submitted color palette, we download the fullsize image with the url originally
derived from the RedwallpaperScraper.

In parts mentioned above, they in whole, form a chain of pipelines that feed
into each other. I recognized that they could all happen independent of each
other, which is why I decided to Thread them. Like a funnel, we get the
following flow of data using thread-safe data structures.
    > RedwallpaperScraper (Queue) - API querying
    > ThumbnailBuffer (Queue) - Thumbnail downloading/resizing
    > ScoredBuffer (Min-Priority Queue) - Scoring
    > FullsizeBuffer (Queue) - Fullsize downloading

Lastly, there's an RedWallpaperImage class that I created, which allows for
an image to be automatically thumbnailed or clustered when instanciated
with either a valid image array, or file.

Because I decided to exclusively use Threading (I don't think this was
the best way to go about it), I had to figure out a way to trip an early to
the four threaded buffers. I created an exit() function that would flag
an end attribute for each buffer, which in turn would raise a 'StopIteration'
exception. Despite try/catch, I do occasionally get an exception error raised
when I end the program. But that's only when a user tries to end the program,
so not a fatal error.

All in all, it was a wonderful learning experience.
With more time, I would have loved to allow a user to interact with a GUI.
e.g. Pick colors via the GUI, preview images, and have a better overall UI
experience. I would love to include more high-res image feeds beyond Reddit.
I wanted to create this as an app that one would be able to run with just
'python redwallpaper' from the CLI, but I didn't have the time to nail down
the overall package hierarchy/structuring. This is very apparent in the
'tests.py' file, where it fails to find the test image. Whereas, the test
script ran perfectly fine when I was developing it in a Jupyter notebook
outside the redwallpaper directory. I had also intended to allow users
to pick colors from an actual palette, but reconsidered with limited time.
And if I still had more time, I'd refactor the entire project
(lol, but actually).

I hope you enjoy testing this (I pray this works on Windows/Linux), and
I hope you find a new and interesting desktop wallpaper!
