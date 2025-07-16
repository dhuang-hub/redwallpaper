import argparse
from redwallpaper.RedWallpaperApp import RedWallpaperApp


def main(argv=None):
    parser = argparse.ArgumentParser(description="Run RedWallpaper")
    parser.parse_args(argv)
    RedWallpaperApp()


if __name__ == '__main__':
    main()
