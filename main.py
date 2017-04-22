import os

import get_urls
import image_downloader
import set_image

# subreddit to pull pictures from
SUBREDDIT = "/r/wallpapers"

# pictures folder path in current working directory (cwd)
FOLDER_PATH = os.getcwd() + "\\pictures\\"


def main(subreddit):
    """
    Gets reddit pic URLs from given subreddit already filtered
	Downloads the pictures
	Sets Desktop Background
	"""
    pic_urls = get_urls.reddit_pics(subreddit)
    image_downloader.check_folder(FOLDER_PATH)
    image_downloader.download_pics(pic_urls, FOLDER_PATH)
    # set_image.set_image(FOLDER_PATH + "2cL5jGL.jpg")


main(SUBREDDIT)
