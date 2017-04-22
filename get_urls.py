import bs4 as bs
import urllib.request


def get_subreddit_urls(subreddit):
    """
    Gets all the urls from the first page of a subreddit
    :return: raw urls to be filtered
    :rtype: set
    """
    soup = get_soup("http://www.reddit.com" + subreddit)
    urls = set()
    errors = 0
    for div in soup.find_all("div", {'data-type': 'link'}):
        try:  # probably not necessary anymore
            url = div.get('data-url', '')
            urls.add(url)
        except KeyError:
            errors += 1
            continue
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


def reddit_pics(subreddit):
    """
    from a subreddit name returns a list of urls of image already filtered
    :param subreddit: r/subreddit name 
    :type subreddit: string
    :return: urls of images
    :rtype: list of strings
    """
    urls = get_subreddit_urls(subreddit)
    pic_urls = filter_urls(urls)
    return pic_urls
