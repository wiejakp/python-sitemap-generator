import threading
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.error import HTTPError
from lxml.html.soupparser import fromstring
from var_dump import var_dump

from data_management import data_manager

types = 'text/html'
request_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Connection": "keep-alive"
}


class Crawl(threading.Thread):

    def __init__(self, index, obj, initial_url_info, dump):
        threading.Thread.__init__(self)

        self.index = index
        self.obj = obj
        self.initial_url_info = initial_url_info

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

                    # var_dump(temp_content)

                    try:
                        temp_data = fromstring(temp_content)
                        temp_thread = threading.Thread(target=self.parse_thread,
                                                       args=(self.obj['url'], temp_data))
                        data_manager.append("linked_threads", temp_thread)
                        temp_thread.start()
                    except (RuntimeError, TypeError, NameError, ValueError):
                        print('Content could not be parsed, perhaps it is XML? We do not support that yet.')
                        # var_dump(temp_content)
                        pass

        except HTTPError as e:
            print('HTTPError: ', self.obj['url'])
            temp_status = e.code
            pass

        except URLError as e:
            print('URLError: ', self.obj['url'])
            temp_status = 000
            pass

        self.obj['obj'] = temp_object
        self.obj['sta'] = temp_status

        data_manager.process_checked(self.obj)

    def parse_thread(self, url, data):
        temp_links = data.xpath('//a')

        for temp_index, temp_link in enumerate(temp_links):
            temp_attrs = temp_link.attrib

            if 'href' in temp_attrs:
                temp_url = temp_attrs.get('href')
                temp_src = url
                temp_value = temp_link.text
                temp_url = temp_attrs.get('href')

                path = data_manager.join_url(temp_src, temp_url, self.initial_url_info)

                if path:
                        data_manager.process_url(path, temp_src)
