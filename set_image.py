import ctypes
import os
import bs4 as bs
import urllib.request

# https://docs.python.org/2/library/os.path.html

SUBREDDIT = "/r/backgrounds"

# pictures folder path in current working directory (cwd)
FOLDER_PATH = os.getcwd() + "/pictures/"

def main():
	pic_urls = get_pic_urls()
	pic_urls, imgur_urls = filter_urls(pic_urls)
	
	# goes to imgur URL and adds pic_urls
	for imgur_url in imgur_urls:
		pic_urls = get_imgur_pic(pic_urls, imgur_url)
		
	for url in pic_urls:
		print(url)
		
	check_folder(FOLDER_PATH)
	download_pics(pic_urls)
	
# Sets the desktop background to the current image path
def set_image(image_path):
    SPI_SETDESKWALLPAPER = 0x14
    SPIF_UPDATEINIFILE = 0x2
    image_path = FOLDER_PATH + image_fname
    #ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, SPIF_UPDATEINIFILE)

# Gets reddit urls (some .jpg and others not)
def get_pic_urls():
    soup = get_soup("http://www.reddit.com"+SUBREDDIT)
    pic_urls = set()
    for div in soup.find_all("div"):
        try:
            url = div["data-url"]
        except KeyError:
            continue
        pic_urls.add(url)
    return pic_urls
	
def get_soup(url):
	hdr = {'User-Agent' : 'super happy bot by /u/GreenMachine'}
	req = urllib.request.Request(url, headers=hdr)
	source = urllib.request.urlopen(req).read()
	soup = bs.BeautifulSoup(source, 'lxml')
	return soup
	
# filters url's into 3 categories
# file types .jpg, .png which are ready to download_pics
# imgur urls that can be reliably searched through
# other urls which are discarded
def filter_urls(urls):
	pic_urls = set()
	imgur_urls = set()
	for url in urls:
		if url.endswith(".jpg") or url.endswith(".png"):
			pic_urls.add(url)
		elif "imgur" in url:
			imgur_urls.add(url)
	return (pic_urls, imgur_urls)
			
# Goes into the imgur link and adds all pictures to pic_urls
def get_imgur_pic(pic_urls, imgur_url):
	soup = get_soup(imgur_url)
	for img in soup.find_all("img"):
		if img["src"].endswith(".jpg") or img["src"].endswith(".png"):
			pic_urls.add(img["src"].strip("//"))
	return pic_urls
	
# makes sure folder exists and creates it if it doesn't
def check_folder(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print("making folder")
    else:
        print("folder already exists")

# downloads the pics to FOLDER_PATH constant
def download_pics(pic_urls):
	for url in pic_urls:
		name = url.split("/")
		name = name[-1]
		try:
			urllib.request.urlretrieve(url, FOLDER_PATH+name)
		except ValueError:
			urllib.request.urlretrieve("http://"+url, FOLDER_PATH+name)
		
# runs main if module was run directly
# won't automatically run if it is imported
if __name__ == "__main__":
    main()