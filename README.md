# Python Sitemap Generator

- Version: 0.4.2
- Update: 2022/12/26

Python Site Map Generator uses python multi-threaded approach to read all links accessible through the Web site and generate proper sitemap for SEO purposes. 
Script was meant to use threading technology to allow easy and very fast approach while generating sitemaps for your Web pages.
The script will run under Linux operating system which supports Python 3 language.

Use with caution, if you set thread count too high, it can cause your web server to bug out and cause some links to throw an error, or your IP will be blocked due to firewall threashold.

## REQUIREMENTS
- Python 3
- lxml
- bs4

## USAGE:
- Install requirements `python3 -m pip install -r requirements.txt`
- Run script with params: `python3 python-sitemap-generator.py -threads 4 -url https://github.com/ -o sitemap.xml`.

![Python Sitemap Generator](https://raw.github.com/wiejakp/python-sitemap-generator/master/screenshot.png)
