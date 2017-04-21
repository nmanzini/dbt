import ctypes
import os
import bs4 as bs
import urllib.request

# https://docs.python.org/2/library/os.path.html

SUBREDDIT = "/r/wallpapers"

# pictures folder path in current working directory (cwd)
FOLDER_PATH = os.getcwd() + "/pictures/"


def main():
    """
    main fucntion that get the urls, filters them, check the folder and download there the pics
    :return: nothing
    :rtype: none
    """
    urls = get_pic_urls()
    pic_urls = filter_urls(urls)
    for url in pic_urls:
        print(url)
    check_folder(FOLDER_PATH)
    download_pics(pic_urls)


# Sets the desktop background to the current image path
def set_image(image_path):

    SPI_SETDESKWALLPAPER = 0x14
    SPIF_UPDATEINIFILE = 0x2
    image_path = FOLDER_PATH + image_fname
    # ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, SPIF_UPDATEINIFILE)


# Gets reddit urls (some .jpg and others not)
def get_pic_urls():
    """
    gets all the urls form the first subreddit page
    :return: raw urls to be filtered
    :rtype: set
    """
    soup = get_soup("http://www.reddit.com"+SUBREDDIT)
    pic_urls = set()
    for div in soup.find_all("div", {'data-type': 'link'}):
        try:                #probably not necessary anymore
            url = div.get('data-url','')
        except KeyError:
            continue
        pic_urls.add(url)
    print('added',len(pic_urls),'pic urls to the url-list')
    return pic_urls


def get_soup(url):
    """
    fast way to get a soup with a custom agent
    :param url: a normal url
    :type url: string
    :return: the soup of that url
    :rtype: soup
    """
    hdr = {'User-Agent': 'super happy bot by /u/GreenMachine'}
    req = urllib.request.Request(url, headers=hdr)
    source = urllib.request.urlopen(req)
    soup = bs.BeautifulSoup(source, 'lxml')
    return soup


# filters url's into 3 categories
# file types .jpg, .png which are ready to download_pics
# imgur urls that can be reliably searched through
# other urls which are discarded
def filter_urls(urls):
    """
    gets a set of raw urls and returns a set of nice urls of images
    :param urls: urls of images and imgur pages or other pages
    :type urls: set
    :return: urls of actual pics
    :rtype: set
    """
    pic_urls = set()
    bad_urls = set()
    for url in urls:
        if url.endswith(".jpg") or url.endswith(".png"):
            pic_urls.add(url)
        elif "imgur" in url:
            pic_urls.add(get_imgur_pic(url))
        else:
            bad_urls.add(url)
            print('rejected',url)
    print('of original',len(urls),'images:',len(pic_urls),'approved,',len(bad_urls),'rejected:')


    return pic_urls


# Goes into the imgur link and adds all pictures to pic_urls
def get_imgur_pic(imgur_url):
    """
    get the first image at full resolution from a  imgur page
    :param imgur_url: imgur page url
    :type imgur_url: string
    :return: imgur image url
    :rtype: string
    """

    soup = get_soup(imgur_url)
    pic_url = 'http:'+soup.find('a', class_='zoom').get('href')
    return pic_url

    '''
    for img in soup.find_all("img"):
        if img["src"].endswith(".jpg") or img["src"].endswith(".png"):
            pic_urls.add(img["src"].strip("//"))
    return pic_urls
    '''


# makes sure folder exists and creates it if it doesn't
def check_folder(directory):
    """
    
    :param directory: 
    :type directory: 
    :return: 
    :rtype: 
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        print("making folder")
    else:
        print("folder already exists")


# downloads the pics to FOLDER_PATH constant
def download_pics(pic_urls):
    """
    
    :param pic_urls: 
    :type pic_urls: 
    :return: 
    :rtype: 
    """
    for url in pic_urls:
        name = url.split("/")[-1]
        try:
            urllib.request.urlretrieve(url, FOLDER_PATH + name)
        except ValueError:
            urllib.request.urlretrieve("http://" + url, FOLDER_PATH + name)


# runs main if module was run directly
# won't automatically run if it is imported

if __name__ == "__main__":
    main()
