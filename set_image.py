import ctypes

def set_image(image_path):
    """
    Changes the desktop background to the image found at the image path
    :return: nothing
    :rtype: none
    """
    print("setting desktop background to " + image_path)
    SPI_SETDESKWALLPAPER = 0x14
    SPIF_UPDATEINIFILE = 0x1
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, SPIF_UPDATEINIFILE)