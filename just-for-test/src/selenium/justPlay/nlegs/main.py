
import sys
sys.path.append(
    r'F:/Code/JustFor_Practice/justfor_practice/just-for-test/src/selenium/justPlay')
import requests
import urllib.request
from pandas import DataFrame
# from bs4 import BeautifulSoup
import lxml.html
import time
import os
# from justPlay.util.constants import ROOT_SAVE_PATH

URL = 'http://nlegs.com/'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
ROOT_FOLDER = "F:/New Folder/craw/"
error_list_path = "F:/New Folder/craw/not_finished.txt"

header = {
    'User-Agent': user_agent
}

RETRY_TIMES = 10


def main(sub_url=None):
    print('***Start in page {}***'.format(sub_url))
    # req = urllib.request.Request(url,headers=header)
    # content = urllib.request.urlopen(req)
    # content.read().decode('utf-8')
    req = requests.get(URL+sub_url, headers=header)
    req.encoding = 'utf-8'
    html = req.text

    dom = lxml.html.fromstring(html)
    # get all the urls for one page
    links = [a for a in dom.xpath(u"//a[contains(@href, 'girls')]/@href")]
    titles = [b for b in dom.xpath(u"//span[@class='title']/text()")]
    unfinished_links = []
    # print(list(zip(links, titles)))

    for target, name in zip(links, titles):
        try:
            craw(target, name)
            main_series = name.split(" ")[0]
            with open(ROOT_FOLDER + main_series + "/" + main_series + ".txt", "a+") as success_file:
                success_file.write('{} {}'.format(target, name))
                success_file.write("\n")
        except BaseException:
            unfinished_links.append((target, name))
        time.sleep(1)

    if unfinished_links:
        print(unfinished_links)
        for source_name_tuple in unfinished_links:
            with open(error_list_path, "a+") as error_file:
                error_file.write('{}|{}'.format(source_name_tuple[0], source_name_tuple[1]))
                error_file.write("\n")
    else:
        print('===All finished for {}==='.format(sub_url))

    # soup = BeautifulSoup(html, 'html.parser')
    # hyperLinks = soup.find_all('li')
    # print(hyperLinks)


def craw(url, name, left_over=None, retry=None):
    name_list = name.split(" ")
    main_series = name_list[0]
    folder_name = " ".join(name_list[1:]).rstrip()
    task_dir = ROOT_FOLDER + main_series + "/" + folder_name.replace('/', '_')
    if not os.path.exists(task_dir):
        os.makedirs(task_dir)
    elif retry == None or not len(os.listdir(task_dir)) == 0:
        print('skip {} {}'.format(url, name))
        return

    if not left_over:
        print('start {}'.format(name))
        request = requests.get(URL + url, headers=header)
        request.encoding = 'utf-8'
        html = request.text
        dom = lxml.html.fromstring(html)
        links = [a for a in dom.xpath(u"//a[contains(@href, 'images')]/@href")]

        finished_links = []
        retry = 0
    else:
        links = left_over
        finished_links = []
        retry = retry

    headers = [('Host', 'nlegs.com'),
               ('Connection', 'keep-alive'),
               ('Cache-Control', 'max-age=0'),
               ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'),
               ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'),
               ('Accept-Encoding', 'gzip,deflate'),
               ('Accept-Language', 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5'),
               ('If-None-Match', "5d88acc7-a837e"),
               ('Referer', URL + url),
               ('If-Modified-Since', 'Thu, 01 Jan 1970 00:00:00 GMT')]

    url_opener = urllib.request.build_opener()
    url_opener.addheaders = headers
    try:
        for index, link in enumerate(links):
            print("downloading {}/{} link={}\r".format(index + 1, len(links), name), end="")
            link_index = link.split('/')[-1].replace('.jpg', '')
            data = url_opener.open(URL + link[1:])
            # req = requests.get(URL + link[1:], headers=header, stream=True)
            # req.raise_for_status()
            with open("{}/{}.jpg".format(task_dir.rstrip(), link_index), "wb") as f:
                f.write(data.read())
                # for chunk in req.iter_content(chunk_size=50000):
                #     f.write(chunk)
            finished_links.append(link)
            time.sleep(0.35)
        print('finish {}'.format(name))
    except Exception as e:
        print(e)
        if retry < RETRY_TIMES:
            for i in range(5):
                print('retry in {} seconds\r'.format(i), end='')
                time.sleep(1)
            craw(url, name, list(set(links) - set(finished_links)), retry + 1)
        else:
            print('Too many retries. try next time. {} {}'.format(url, name))
            with open(error_list_path, "wb") as error_file:
                error_file.write('{} {}'.format(url, name))
                error_file.write("\n")
            return


if __name__ == "__main__":
    for i in range(1,3):
        main(sub_url='model/{}.html'.format(i))


# (Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3
# Accept-Encoding: gzip, deflate
# Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,ja;q=0.5
# Cache-Control: max-age=0
# Connection: keep-alive
# Cookie: __cfduid=d99098768193d91bf2a6087682927c7cc1569212362
# Host: nlegs.com
# If-Modified-Since: Mon, 23 Sep 2019 11:30:15 GMT
# If-None-Match: "5d88acc7-a837e"
# Referer: 'http://nlegs.com/girls/2019/09/23/12291.html'
# Upgrade-Insecure-Requests: 1
# User-Agent:
