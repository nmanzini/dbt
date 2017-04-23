import os

import get_urls
import image_downloader
#import schedule
import time
import set_image

# subreddit to pull pictures from
SUBREDDITS = ["wallpapers", "EarthPorn", "WQHD_Wallpaper"]

# pictures folder path in current working directory (cwd)
FOLDER_PATH = os.getcwd() + "\\pictures\\"

# number of pages to go through (up to 25 pictures per page)
PAGES = 3


def main():
    """
    Gets reddit pic URLs from given subreddit already filtered
	Downloads the pictures
	Sets Desktop Background
	"""
    pic_urls = get_urls.reddit_pics(SUBREDDITS, PAGES)
    image_downloader.check_folder(FOLDER_PATH)
    image_downloader.download_pics(pic_urls, FOLDER_PATH)

    #list of file in the pictures folder
    images = [file for file in os.listdir(FOLDER_PATH)]

    #code with schedule library
    #schedule.every(10).seconds.do(set_back, images)
    while len(images) > 0:
        #schedule.run_pending()
        set_back(images)
        time.sleep(5)


def set_back(images_list):
    """
    function that pops an image from the list ad sets it as background
    :param images_list: names of images
    :type images_list: string
    :return: changes background
    :rtype: none
    """
    image = images_list.pop()
    set_image.set_image(FOLDER_PATH+image)


main()

