import os
import urllib.request


def check_folder(directory):
    """
    Makes sure folder exists and creates it if it doesn't
    :param directory: absolute path to folder to check for
    :type directory: string
    :return: N/A
    :rtype: N/A
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        print("making pictures folder")
        print()
    else:
        print("pictures folder already exists")
        print()


def download_pics(pic_urls, directory):
    """
    Pictures are placed in current directory/pictures/
    :param pic_urls: set of valid .jpg or .png URLs
    :type pic_urls: set
    :param directory: path to folder pictures will be placed into
    :type directory: string
    :return: N/A
    :rtype: N/A
    """
    print("downloading pictures...")
    for url in pic_urls:
        name = url.split("/")[-1]
        if len(name) >= 20:
            name = name[len(name)-20:]
    
        print('from:', url)
        pic_path = directory + name
        if not os.path.exists(pic_path):
            print("downloading ->", pic_path)
            try:
                urllib.request.urlretrieve(url, pic_path)
            except ValueError:
                # 'http://' missing from link
                urllib.request.urlretrieve("http://" + url, pic_path)
            except urllib.error.HTTPError:
                # access forbidden
                # ex: http://puu.sh/n2zPL/2491975ef3.jpg
                print("URL skipped due to HTTPError", url)
        else:
            print("already downloaded ->", pic_path)
    print("Downloads Finished")
