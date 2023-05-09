from urllib.parse import urljoin, quote
from urllib.parse import urlparse


class DataManagement:

    def __init__(self):

        self.data = {
            "threads": [],
            "linked_threads": [],
            "queue": [],
            "checked": [],
        }

    def append(self, key, value):
        self.data[key].append(value)

    def delete(self, key, index):
        del self.data[key][index]

    def get(self, key):
        return self.data[key]

    def len(self, key):
        return len(self.data[key])

    def process_url(self, url, src=None, obj=None):
        found = False

        for value in self.get("queue"):
            if value['url'] == url:
                found = True
                break

        for value in self.get("checked"):
            if value['url'] == url:
                found = True
                break

        if not found:
            temp = {'url': url, 'src': src, 'obj': obj, 'sta': None}

            self.append("queue", temp)

    def process_checked(self, obj):
        found = False

        for item in self.get("checked"):
            if item['url'] == obj['url']:
                found = True
                break

        if not found:
            self.append("checked", obj)

    def join_url(self, src, url, initial_url_info):

        initial_url_base = initial_url_info["initial_url_base"]
        initial_url_netloc = initial_url_info["initial_url_netloc"]
        netloc_prefix_str = initial_url_info["netloc_prefix_str"]
        netloc_prefix_len = initial_url_info["netloc_prefix_len"]

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

        if url_netloc == '' or url_netloc == initial_url_netloc:

            url_path = url_info.path
            if "%" not in url_path:
                url_path = quote(url_path, safe="/:&?=#")

            src_path = src_info.path
            if "%" not in src_path:
                src_path = quote(src_path, safe="/:&?=#")

            if url_info.query:
                url_path = url_path + '?' + url_info.query

            src_new_path = urljoin(initial_url_base, src_path)
            url_new_path = urljoin(src_new_path, url_path)

            path = urljoin(src_new_path, url_new_path)

            if path[-1] != "/":
                path += "/"
            # print path

            value = path

        return value


data_manager = DataManagement()
