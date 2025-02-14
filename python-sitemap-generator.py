#!/usr/bin/python

# Python Sitemap Generator
# Version: 0.4.2

# Przemek Wiejak
# GitHub: https://github.com/wiejakp/python-sitemap-generator

import threading
import time
import argparse

from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.request import HTTPError
from urllib.parse import urljoin
from urllib.parse import urlparse

import email.utils as eut

from pprint import pprint
from lxml import etree
from lxml.html.soupparser import fromstring

queue = []
checked = []
threads = []
types = 'text/html'

link_threads = []

# adjust to your liking but keep values low to prevent firewalls blocking you for flooding
# or using up all of your web server resources.

netloc_prefix_str = 'www.'
netloc_prefix_len = len(netloc_prefix_str)

run_ini = None
run_end = None
run_dif = None

request_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Connection": "keep-alive"
}


class RunCrawler(threading.Thread):
    # crawler start
    run_ini = time.time()
    run_end = None
    run_dif = None


    def __init__(self, url):
        threading.Thread.__init__(self)

        ProcessURL(url)

        self.start()

    def run(self):
        run = True

        while run:
            for index, thread in enumerate(threads):
                if thread.is_alive() == False:
                    del threads[index]

            for index, thread in enumerate(link_threads):
                if thread.is_alive() == False:
                    del link_threads[index]

            for index, obj in enumerate(queue):
                if len(threads) < MaxThreads:
                    thread = Crawl(index, obj)
                    threads.append(thread)

                    del queue[index]
                else:
                    break

            if len(queue) == 0 and len(threads) == 0 and len(link_threads) == 0:
                run = False

                self.done()
            else:
                print ('Threads: ', len(threads), ' Queue: ', len(queue), ' Checked: ', len(checked), ' Link Threads: ', len(link_threads) + 1)
                time.sleep(1)

    def done(self):
        print ('Checked: ', len(checked))
        print ('Running XML Generator...')

        # Running sitemap-generating script
        Sitemap()

        self.run_end = time.time()
        self.run_dif = self.run_end - self.run_ini

        print(self.run_dif)


class Sitemap:
    urlset = None
    encoding = 'UTF-8'
    xmlns = 'http://www.sitemaps.org/schemas/sitemap/0.9'

    def __init__(self):
        self.root()
        self.children()
        self.xml()

    def done(self):
        print ('Done')

    def root(self):
        self.urlset = etree.Element('urlset')
        self.urlset.attrib['xmlns'] = self.xmlns

    def children(self):
        for index, obj in enumerate(checked):
            url = etree.Element('url')
            loc = etree.Element('loc')
            lastmod = etree.Element('lastmod')
            changefreq = etree.Element('changefreq')
            priority = etree.Element('priority')

            loc.text = obj['url']
            lastmod_info =  None
            lastmod_header = None
            lastmod.text = None

            if hasattr(obj['obj'], 'info'):
                lastmod_info = obj['obj'].info()
                lastmod_header = lastmod_info["Last-Modified"]


            # check if 'Last-Modified' header exists
            if lastmod_header != None:
                lastmod.text = FormatDate(lastmod_header)

            if loc.text != None:
                url.append(loc)

            if lastmod.text != None:
                url.append(lastmod)

            if changefreq.text != None:
                url.append(changefreq)

            if priority.text != None:
                url.append(priority)

            self.urlset.append(url)

    def xml(self):
        f = open(filename, 'w')
        
        print (etree.tostring(self.urlset, pretty_print=True, encoding="unicode", method="xml"), file=f)
        f.close()

        print ('Sitemap saved in: ', filename)


class Crawl(threading.Thread):
    def __init__(self, index, obj):
        threading.Thread.__init__(self)

        self.index = index
        self.obj = obj

        self.start()


    def run(self):
        temp_status = None
        temp_object = None

        try:
            temp_req = Request(self.obj['url'], headers=request_headers)
            temp_res = urlopen(temp_req)
            temp_code = temp_res.getcode()
            temp_type = temp_res.info()["Content-Type"]

            temp_status = temp_res.getcode()
            temp_object = temp_res

            if temp_code == 200:
                if types in temp_type:
                    temp_content = temp_res.read()


                    try:
                        temp_data = fromstring(temp_content)
                        temp_thread = threading.Thread(target=ParseThread, args=(self.obj['url'], temp_data))
                        link_threads.append(temp_thread)
                        temp_thread.start()
                    except (RuntimeError, TypeError, NameError, ValueError):
                        print ('Content could not be parsed, perhaps it is XML? We do not support that yet.')
                        pass

        except URLError as e:
            print ('URLError: ', self.obj['url'])
            temp_status = 000
            pass

        except HTTPError as e:
            print ('HTTPError: ', self.obj['url'])
            temp_status = e.code
            pass

        self.obj['obj'] = temp_object
        self.obj['sta'] = temp_status

        ProcessChecked(self.obj)


def dump(obj):
    '''return a printable representation of an object for debugging'''
    newobj=obj

    if '__dict__' in dir(obj):
      newobj=obj.__dict__

      if ' object at ' in str(obj) and not newobj.has_key('__type__'):
          newobj['__type__']=str(obj)

          for attr in newobj:
              newobj[attr]=dump(newobj[attr])

    return newobj


def FormatDate(datetime):
    datearr = eut.parsedate(datetime)
    date = None

    try:
        year = str(datearr[0])
        month = str(datearr[1])
        day = str(datearr[2])

        if int(month) < 10:
            month = '0' + month

        if int(day) < 10:
            day = '0' + day

        date = year + '-' + month + '-' + day
    except IndexError:
        pprint(datearr)

    return date


def ParseThread(url, data):
    temp_links = data.xpath('//a')

    for temp_link in temp_links:
        temp_attrs = temp_link.attrib

        if 'href' in temp_attrs:
            temp_url = temp_attrs.get('href')
            temp_src = url
            temp_value = temp_link.text
            temp_url = temp_attrs.get('href')

            path = JoinURL(temp_src, temp_url)

            if path != False:
                ProcessURL(path, temp_src)


def JoinURL(src, url):
    value = False

    url_info = urlparse(url)
    src_info = urlparse(src)

    url_scheme = url_info.scheme
    src_scheme = src_info.scheme

    url_netloc = url_info.netloc
    src_netloc = src_info.netloc

    if src_netloc.startswith(netloc_prefix_str):
        src_netloc = src_netloc[netloc_prefix_len:]

    if url_netloc.startswith(netloc_prefix_str):
        url_netloc = url_netloc[netloc_prefix_len:]

    if url_netloc == '' or url_netloc == InitialURLNetloc:
        url_path = url_info.path
        src_path = src_info.path

        if url_info.query:
            url_path = url_path + '?' + url_info.query

        src_new_path = urljoin(InitialURLBase, src_path)
        url_new_path = urljoin(src_new_path, url_path)

        path = urljoin(src_new_path, url_new_path)

        #print path

        value = path

    return value


def ProcessURL(url, src = None, obj = None):
    found = False

    for value in queue:
        if value['url'] == url:
            found = True
            break

    for value in checked:
        if value['url'] == url:
            found = True
            break

    if found == False:
        temp = {}
        temp['url'] = url
        temp['src'] = src
        temp['obj'] = obj
        temp['sta'] = None

        queue.append(temp)

def ProcessChecked(obj):
    found = False

    for item in checked:
        if item['url'] == obj['url']:
            found = True
            break

    if found == False:
        checked.append(obj)
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some URLs.')
    parser.add_argument('-url', type=str, required=True, help='The URL to start crawling from')
    parser.add_argument('-threads', type=int, default=4, required=False, help='The number of threads to use for crawling (default: 4).')
    parser.add_argument('-o', type=str, default="sitemap.xml", required=False, help='The output file to save the sitemap to (default: sitemap.xml).')
    
    args = parser.parse_args()
    
    MaxThreads = args.threads
    InitialURL = args.url
    filename = args.o
    
    InitialURLInfo = urlparse(InitialURL)
    InitialURLLen = len(InitialURL.split('/'))
    InitialURLNetloc = InitialURLInfo.netloc
    InitialURLScheme = InitialURLInfo.scheme
    InitialURLBase = InitialURLScheme + '://' + InitialURLNetloc
    
    if InitialURLNetloc.startswith(netloc_prefix_str):
        InitialURLNetloc = InitialURLNetloc[netloc_prefix_len:]

    

    RunCrawler(InitialURL)
