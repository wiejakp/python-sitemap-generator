import time
from urllib.parse import urlparse
from data_management import data_manager
from crawler import Crawl
from sitemap import Sitemap
from argparse import ArgumentParser


class RunCrawler:

    def __init__(self, url, max_threads, filename, initial_url_info, dump):
        self.max_threads = max_threads
        self.init_time = time.time()
        self.filename = filename
        self.initial_url_info = initial_url_info
        self.dump = dump

        data_manager.process_url(url)

    def start_crawling(self):
        run = True

        while run:
            for index, thread in enumerate(data_manager.get("threads")):
                if not thread.is_alive():
                    data_manager.delete("threads", index)

            for index, thread in enumerate(data_manager.get("linked_threads")):
                if not thread.is_alive():
                    data_manager.delete("linked_threads", index)

            for index, obj in enumerate(data_manager.get("queue")):
                if data_manager.len("threads") < self.max_threads:
                    new_thread = Crawl(index, obj, self.initial_url_info, self.dump)
                    data_manager.append("threads", new_thread)

                    data_manager.delete("queue", index)

                else:
                    break

            if data_manager.len("queue") == 0 and data_manager.len("threads") == 0 and data_manager.len(
                    "linked_threads") == 0:
                run = False

                self.done()
            else:
                print('Threads: ', data_manager.len("threads"), ' Queue: ', data_manager.len("queue"), ' Checked: ',
                      data_manager.len("checked"),
                      ' Link Threads: ',
                      data_manager.len("linked_threads") + 1)
                time.sleep(1)

    def done(self):
        print('Checked: ', data_manager.len("checked"))
        print('Running XML Generator...')

        # Running sitemap-generating script
        Sitemap().generate_and_save_sitemap(data_manager.get("checked"), self.filename)

        print(f"Elapsed Time: {time.time() - self.init_time}")


def parse_url(url: str):
    url = url.lower()
    if not url.startswith("https://"):
        url = "https://" + url

    if not url.endswith("/"):
        url += "/"

    url_parsed = urlparse(url)
    url_netloc = url_parsed.netloc
    url_scheme = url_parsed.scheme
    url_base = url_scheme + '://' + url_netloc

    netloc_prefix_str = 'www.'
    netloc_prefix_len = len(netloc_prefix_str)

    if url_netloc.startswith(netloc_prefix_str):
        url_netloc = url_netloc[netloc_prefix_len:]

    url_info = {
        "initial_url_base": url_base,
        "initial_url_netloc": url_netloc,
        "netloc_prefix_str": netloc_prefix_str,
        "netloc_prefix_len": netloc_prefix_len,
    }

    return url, url_info


if __name__ == "__main__":

    parser = ArgumentParser(description="A python Site Map Generator, that crawl any webpage and generate XML sitemap "
                                        "compatible with Google's indexing robot.")

    parser.add_argument("-u", "--url", required=True, type=str)
    parser.add_argument("-f", "--filename", default="sitemap.xml", type=str)
    parser.add_argument("-mt", "--max-threads", default=4, type=int)
    parser.add_argument("-d", "--dump", default=-1, help="To show html of pages in console. To enable set it to 1. The default is -1.")
    args = parser.parse_args()

    url = args.url
    max_threads = args.max_threads
    filename = args.filename
    dump = True if int(args.dump) > 0 else False

    initial_url, initial_url_info = parse_url(url)

    run_crawler = RunCrawler(initial_url, max_threads, filename, initial_url_info, dump)
    run_crawler.start_crawling()
