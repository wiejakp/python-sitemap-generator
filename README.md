# Python Sitemap Generator

- Version: 0.4
- Update: 22/22/2021
- Author: Przemek Wiejak @ przemek@wiejak.app

Python Site Map Generator uses python multi-threaded approach to read all links accessible through the Web site and generate proper sitemap for SEO purposes. 
Script was meant to use threading technology to allow easy and very fast approach while generating sitemaps for your Web pages.
The script will run under Linux operating system which supports Python 3 language.

## REQUIREMENTS
- Python 3
- sudo apt-get install python-beautifulsoup
- sudo apt-get install python-pip
- sudo apt-get install python3-pip
- pip install setuptools
- pip install var_dump

## USAGE:
- Set up the 'InitialURL' variable to point to Web site which you want to generate sitemap to
- Set script to executable: sudo chmod +x python-sitemap-generator.py
- Run script: ./python-sitemap-generator.py

![Python Sitemap Generator](https://raw.github.com/wiejakp/python-sitemap-generator/master/screenshot.png)
