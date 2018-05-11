#!/usr/bin/python

# Python Sitemap Generator
# Version: 0.2
# Przemyslaw M. Wiejak @ przemek@wiejak.us

import threading
import urlparse
import urllib2
import time
import email.utils as eut

from lxml import etree
from urlparse import urlparse
from lxml.html.soupparser import fromstring
from urlparse import urljoin

# sudo apt-get install python-beautifulsoup

queue = []
checked = []
threads = []
types = ['text/html']

link_threads = []

MaxThreads = 30
MaxSubThreads = 10 

InitialURL = 'WEBSITE ADDRESS'

InitialURLInfo = urlparse(InitialURL)
InitialURLLen = len(InitialURL.split('/'))
InitialURLNetloc = InitialURLInfo.netloc
InitialURLScheme = InitialURLInfo.scheme
InitialURLBase = InitialURLScheme + '://' + InitialURLNetloc

netloc_prefix_str = 'www.'
netloc_prefix_len = len(netloc_prefix_str)

filename = 'sitemap.xml'

request_headers = {
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "http://thewebsite.com",
    "Connection": "keep-alive" 
}

if InitialURLNetloc.startswith(netloc_prefix_str):
    InitialURLNetloc = InitialURLNetloc[netloc_prefix_len:]

class RunCrawler(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        
        ProcessURL(url)
        
        self.start()
            
    def run(self):
        run = True
        
        while run:
            for index, thread in enumerate(threads):
                if thread.isAlive() == False:
                    del threads[index]
                    
            for index, thread in enumerate(link_threads):
                if thread.isAlive() == False:
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
                print 'Threads: ', len(threads), ' Queue: ', len(queue), ' Checked: ', len(checked), ' Link Threads: ', len(link_threads)
                time.sleep(1)
                
    def done(self):        
        print 'Checked: ', len(checked)
        print 'Running XML Generator...'
        
        # Running sitemap-generating script
        Sitemap()
        
class Sitemap:
    urlset = None
    encoding = 'UTF-8'
    xmlns = 'http://www.sitemaps.org/schemas/sitemap/0.9'
    
    def __init__(self):
        self.root()
        self.children()
        self.xml()
                
    def done(self):
        print 'Done'
        
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
            lastmod.text = FormatDate(obj['obj'].info().getheader('Last-Modified'))
            
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
        print >> f, etree.tostring(self.urlset, xml_declaration = True, encoding = self.encoding)
        f.close()
        
        print 'Sitemap saved in: ', filename
            
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
            temp_req = urllib2.Request(self.obj['url'], headers=request_headers)
            temp_res = urllib2.urlopen(temp_req)
            temp_code = temp_res.getcode()
            temp_type = temp_res.info().type
            
            temp_status = temp_res.getcode()
            temp_object = temp_res
                        
            if temp_code == 200:
                if temp_type in types:
                    temp_content = temp_res.read()
                    temp_data = fromstring(temp_content)

                    temp_thread = threading.Thread(target=ParseThread, args=(self.obj['url'], temp_data))
                    link_threads.append(temp_thread)
                    temp_thread.start()
                    
        except urllib2.HTTPError as e:
            temp_status = e.code
            pass
        
        self.obj['obj'] = temp_object
        self.obj['sta'] = temp_status
        
        ProcessChecked(self.obj)

def FormatDate(datetime):
    datearr = eut.parsedate(datetime)

    year = str(datearr[0])
    month = str(datearr[1])
    day = str(datearr[2])

    if int(month) < 10:
        month = '0' + month

    if int(day) < 10:
        day = '0' + day

    date = year + '-' + month + '-' + day
    
    return date
        
def ParseThread(url, data):
    temp_links = data.xpath('//a')

    for temp_index, temp_link in enumerate(temp_links):
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
    
RunCrawler(InitialURL)
