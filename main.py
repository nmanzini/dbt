import os

import get_reddit_pic_urls
import image_downloader
import set_image

# subreddit to pull pictures from
SUBREDDIT = "/r/wallpapers"

# pictures folder path in current working directory (cwd)
FOLDER_PATH = os.getcwd() + "\\pictures\\"

def main():
    """
    Gets reddit URLs from given SUBREDDIT
	Filters them into usable .jpg and .png
	Downloads the pictures
	Sets Desktop Background
    """
    urls = get_reddit_pic_urls.get_pic_urls(SUBREDDIT)
    pic_urls = get_reddit_pic_urls.filter_urls(urls)

    image_downloader.check_folder(FOLDER_PATH)
    image_downloader.download_pics(pic_urls, FOLDER_PATH)
    #set_image.set_image(FOLDER_PATH + "2cL5jGL.jpg")
	
	
if __name__ == "__main__":
    main()