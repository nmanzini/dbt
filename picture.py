from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

IMG_PATH = "pictures/fvEXlE7.jpg"
WEATHER_PATH = "pictures/weather.png"

MSG = "Let there be light!"

def add_txt(msg, im):
    """
    Adds text to image
    :param msg: txt str to be written
    :param im: Image object to be drawn on
    """

    d = ImageDraw.Draw(im)
    fnt = ImageFont.truetype("arial.ttf", 100)

    # locates txt location based on size of image and size of txt
    im_w, im_h = im.size
    txt_w, txt_h = d.textsize(msg, font=fnt)

    # draw border
    for i in range(-4, 5, 4):
        for j in range(-4, 5, 4):
            txt_loc = ((im_w - txt_w)/2 + i, (im_h - txt_h)/3 + j)
            d.text((txt_loc), msg, font=fnt, fill="black")

    # draw txt
    txt_loc = ((im_w - txt_w) / 2, (im_h - txt_h) / 3)
    d.text((txt_loc), msg, font=fnt, fill="white")

def add_weather(WEATHER_PATH, im):
    """
    Adds weather (wx) to image
    :param msg: txt str to be written
    :param im: Image object to be drawn on
    """
    wx = Image.open(WEATHER_PATH)
    wx.resize((400,400), Image.LANCZOS)

    im_h, im_w = im.size
    wx_h, wx_w = wx.size
    wx_loc = (im_h - wx_h, im_w - wx_w)
    im.paste(wx, wx_loc)

im = Image.open(IMG_PATH)

add_txt(MSG, im)
add_weather(WEATHER_PATH, im)

im.save("copy.jpg")
im.show()