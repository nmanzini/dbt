import bs4 as bs
import urllib.request


def reddit_pics(subreddits, pages, sorting, time_period):
    """
    From a list of subreddits, returns a list of urls of .jpg and .png images
    :param subreddits: list of subreddit strings
    :type subreddits: list
    :param pages: num of pages to search through
    :type pages: int
    :param sorting: method of sorting ex: hot, top, new
    :type sorting: string
    :return: urls of images
    :rtype: list of strings
    """
    # commented only for testing of gui
    # test_existance(subreddits)
    combined_url = build_url(subreddits, pages, sorting, time_period)
    
    urls = get_subreddit_urls(combined_url, pages)
    pic_urls = filter_urls(urls)
    return pic_urls

def build_url(subreddits, pages, sorting, time_period):
    """
    Builds a complete URL based off of parameters given.
    :param subreddits: string made of subs name divided by +
    :type subreddits: string 
    :param pages: num of pages to search through
    :type pages: int
    :param sorting: method of sorting (ex: hot, top, new)
    :type sorting: string
    :param time_period: range of time for links (ex. past week)
    :type time_period: string
    :return: combined url
    :rtype: string
    """
    # combine subreddits into one url containing links from all of them
    subreddits = subreddits.split('+')
    combined_url = "https://www.reddit.com/r/" + subreddits[0]
    '''
    for subreddit in subreddits[1:]:
        combined_url += "+" + subreddit
    '''
    # validate sorting and add it to the end of the url
    sorting_choices = ("hot", "new", "controversial", "top", "gilded", "promoted")
    try:
        assert sorting in sorting_choices
    except AssertionError:
        print("sorting must be one of these choices")
        print(sorting_choices)
    combined_url += ("/" + sorting + "/?sort=" + sorting)
    
    # validate time_period and adding to url
    time_choices = ("hour", "day", "week", "month", "all")
    try:
        assert time_period in time_choices
    except AssertionError:
        print("time_period must be one of these choices")
        print(time_choices)
    combined_url += "&t=" + time_period
    
    return combined_url
    
def test_existance(subreddits):
    ''' 
    Tests if given subreddit exists
    raises exception if they don't exist
    '''
    for subreddit in subreddits:
        url = "https://www.reddit.com/r/" + subreddit
        try:
            soup = get_soup(url)
        except urllib.error.HTTPError:
            raise Exception("/r/" + subreddit + " doesn't exist")
	
        num_links = len(soup.find_all("div", {'data-type': 'link'}))
        if num_links < 1:
            raise Exception("/r/" + subreddit + " has no links")

def get_subreddit_urls(subreddit_url, pages):
    """
    Gets all the picture urls from a given # of pages
    :return: raw urls to be filtered
    :rtype: set
    """
    print(subreddit_url)
    urls = set()
    errors = 0
    current_page = subreddit_url
    soup = get_soup(current_page)
    for i in range(pages):
        if i > 0:
            current_page = subreddit_url + "&count=" + str(i*25) + "&after=" + prev_id
            soup = get_soup(current_page)
        print("getting urls from", current_page)
        
        links = soup.find_all("div", {'data-type': 'link'})
        for link in links:
            url = link.get('data-url', '')
            urls.add(url)
        prev_id = links[-1]["data-fullname"]
        
    print('added', len(urls), 'pic urls to the url-list.', errors, 'errors.')
    return urls


def filter_urls(urls):
    """
    Filters raw URLs into only valid .jpg or .png images.
    get urls from imgur pages
    discard everything else
    :param urls: urls of images and imgur pages or other pages
    :type urls: set
    :return: urls of actual pics
    :rtype: set
    """
    pic_urls = set()
    bad_urls = set()
    for url in urls:
        if url.endswith(".jpg") or url.endswith(".jpeg") or url.endswith(".png"):
            pic_urls.add(url)

        elif url.endswith(".jpg?1"):
            pic_urls.add(url[:-2])
	
        elif url.endswith(".gif") or url.endswith(".gifv"):
            bad_urls.add(url)
			
        elif "imgur.com" in url:
            pic = get_imgur(url)
            if pic:
                pic_urls.add(pic)
            else:
                bad_urls.add(url)

        elif "flickr.com" in url:
            pic = get_flickr(url)
            pic_urls.add(pic)

        elif "i.reddituploads.com" in url:
            pic_urls.add(url+".jpg")

        else:
            bad_urls.add(url)
            print('rejected', url)
    print('of original', len(urls), 'images:', len(pic_urls), 'approved,', len(bad_urls), 'rejected:')

    return pic_urls


def get_imgur(imgur_url):
    """
    Goes into the imgur page url and returns the first valid picture
    :param imgur_url: imgur page url
    :type imgur_url: string
    :return: imgur image url
    :rtype: string
    """
    print("get imgur pic from: " + imgur_url)
    
    try:
        soup = get_soup(imgur_url)
    except urllib.error.HTTPError:
        print("This link has been removed:", imgur_url)
        return

    zoomed_pic = soup.find("a", class_="zoom")
    if zoomed_pic:
        pic_url = "http:" + zoomed_pic.get('href')
    else:
        unzoomed_pic = soup.find("img", itemprop="contentURL")
        pic_url = unzoomed_pic["src"]
    return pic_url


def get_flickr(flickr_url):
    """
    Goes into the flickr page url and returns the first valid picture
    :param flickr_url: imgur page url
    :type flickr_url: string
    :return: flickr image url
    :rtype: string
    """
    print("get flickr pic from: " + flickr_url)
    soup = get_soup(flickr_url)
    zoomed_pic = soup.find("img", class_="zoom-large")

    if zoomed_pic:
        pic_url = "http:" + zoomed_pic["src"]
    else:
        main_pic = soup.find("img", class_="main-photo")
        pic_url = "http:" + main_pic["src"]
    return pic_url


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
