from lxml import etree
from pprint import pprint
import email.utils as eut


class Sitemap:

    def __init__(self):

        self.urlset = None
        self.num_urls = 0
        self.encoding = 'UTF-8'
        self.xmlns = 'http://www.sitemaps.org/schemas/sitemap/0.9'

    def generate_and_save_sitemap(self, checked_urls, filename):

        self.num_urls = len(checked_urls)
        self.urlset = etree.Element('urlset')
        self.urlset.attrib['xmlns'] = self.xmlns

        self._children(checked_urls)
        self._save_xml(filename)

    def _children(self, checked_urls):
        for index, obj in enumerate(checked_urls):
            url = etree.Element('url')
            loc = etree.Element('loc')
            lastmod = etree.Element('lastmod')
            changefreq = etree.Element('changefreq')
            priority = etree.Element('priority')

            loc.text = obj['url']
            lastmod_info = None
            lastmod_header = None
            lastmod.text = None

            if hasattr(obj['obj'], 'info'):
                lastmod_info = obj['obj'].info()
                lastmod_header = lastmod_info["Last-Modified"]

            # check if 'Last-Modified' header exists
            if lastmod_header is not None:
                lastmod.text = self._format_date(lastmod_header)

            if loc.text is not None:
                url.append(loc)

            if lastmod.text is not None:
                url.append(lastmod)

            if changefreq.text is not None:
                url.append(changefreq)

            if priority.text is not None:
                url.append(priority)

            self.urlset.append(url)

    def _save_xml(self, filename):
        f = open(filename, 'w')

        print(etree.tostring(self.urlset, pretty_print=True, encoding="unicode", method="xml"), file=f)
        f.close()

        print(f"Number of saved urls: {self.num_urls}")
        print('Sitemap saved in: ', filename)

    def _format_date(self, datetime):
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
