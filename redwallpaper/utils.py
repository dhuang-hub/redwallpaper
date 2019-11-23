def is_img_ext(file):
    """
    Determines existence of a .jpg or .png file extension from a url string
    """
    return file[-4:] in {'.jpg','.png'} 