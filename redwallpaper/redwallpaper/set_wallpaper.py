import os
import platform
try:
    import appscript
except Exception:  # pragma: no cover - optional dependency
    appscript = None
import ctypes



class UnidentifiedSystem(Exception):
    """Raise when computer operating system is unidentifiable"""
    pass


def set_wallpaper(filepath):
    """
    Provided a filepath to an image, this function will set the wallpaper of the computer.
    Portable for Windows, Linux, and OS.
    """
    plt = platform.system()

    if plt == 'Windows':
        ctypes.windll.user32.SystemParametersInfoW(20, 0, filepath , 3)

    elif plt == 'Linux':
        set_cmd = "/usr/bin/gsettings set org.gnome.desktop.background picture-uri file:"+filepath
        os.system(set_cmd)

    elif plt == 'Darwin':
        if appscript is None:
            raise ImportError('appscript is required on macOS to set wallpapers')
        # For setting the desktops of multiple monitors
        se = appscript.app('System Events')
        desktops = se.desktops.display_name.get()
        for d in desktops:
            desk = se.desktops[appscript.its.display_name == d]
            desk.picture.set(appscript.mactypes.File(filepath))

    else:
        raise UnidentifiedSystem