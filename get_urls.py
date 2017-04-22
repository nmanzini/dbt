import bs4 as bs
import urllib.request


def reddit_pics(subreddits, pages):
    """
    from a subreddit name returns a list of urls of image already filtered
    :param subreddit: r/subreddit name 
    :type subreddit: string
    :return: urls of images
    :rtype: list of strings
    """
    test_existance(subreddits)
	
    combined_url = "https://www.reddit.com/r/" + subreddits[0]
    for subreddit in subreddits[1:]:
        combined_url += "+" + subreddit
    	
    urls = get_subreddit_urls(combined_url, pages)
    pic_urls = filter_urls(urls)
    return pic_urls
	
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

    urls = set()
    errors = 0
    current_page = subreddit_url
    soup = get_soup(current_page)
    for i in range(pages):
        if i > 0:
            current_page = subreddit_url + "/?count=" + str(i*25) + "&after=" + prev_id
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
        if url.endswith(".jpg") or url.endswith(".png"):
            pic_urls.add(url)
        elif "imgur" in url:
            pic_urls.add(get_imgur_pic(url))
        else:
            bad_urls.add(url)
            print('rejected', url)
    print('of original', len(urls), 'images:', len(pic_urls), 'approved,', len(bad_urls), 'rejected:')

    return pic_urls


def get_imgur_pic(imgur_url):
    """
    Goes into the imgur page url and returns the first valid picture
    :param imgur_url: imgur page url
    :type imgur_url: string
    :return: imgur image url
    :rtype: string
    """
    soup = get_soup(imgur_url)
    pic_url = 'http:' + soup.find('a', class_='zoom').get('href')
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
