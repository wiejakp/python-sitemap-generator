import time
from urllib.parse import urlparse

from data_management import data_manager
from crawler import Crawl
from sitemap_generator import Sitemap


class RunCrawler:

    def __init__(self, url, max_threads, filename, initial_url_info):
        self.max_threads = max_threads
        self.init_time = time.time()
        self.filename = filename
        self.initial_url_info = initial_url_info

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
                    new_thread = Crawl(index, obj, self.initial_url_info)
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


if __name__ == "__main__":
    MaxThreads = 4

    # DEFINE YOUR URL - CUSTOM URL!
    InitialURL = 'https://ino.school/'

    InitialURLParsed = urlparse(InitialURL)
    InitialURLLen = len(InitialURL.split('/'))
    InitialURLNetloc = InitialURLParsed.netloc
    InitialURLScheme = InitialURLParsed.scheme
    InitialURLBase = InitialURLScheme + '://' + InitialURLNetloc

    netloc_prefix_str = 'www.'
    netloc_prefix_len = len(netloc_prefix_str)

    if InitialURLNetloc.startswith(netloc_prefix_str):
        InitialURLNetloc = InitialURLNetloc[netloc_prefix_len:]

    InitialURLInfo = {
        "initial_url_base": InitialURLBase,
        "initial_url_netloc": InitialURLNetloc,
        "netloc_prefix_str": netloc_prefix_str,
        "netloc_prefix_len": netloc_prefix_len,
    }
    filename = 'sitemap.xml'

    run_crawler = RunCrawler(InitialURL, MaxThreads, filename, InitialURLInfo)
    run_crawler.start_crawling()
