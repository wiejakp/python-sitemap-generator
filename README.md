# Python Sitemap Generator

- Version: 0.4.2
- Update: 2022/12/26

Python Site Map Generator uses python multi-threaded approach to read all links accessible through the Web site and generate proper sitemap for SEO purposes. 
Script was meant to use threading technology to allow easy and very fast approach while generating sitemaps for your Web pages.
The script will run under Linux operating system which supports Python 3 language.

Use with caution, if you set thread count too high, it can cause your web server to bug out and cause some links to throw an error, or your IP will be blocked due to firewall threashold.

## REQUIREMENTS
The code is updated to newer version. Now it supports `python 3.9`. Now you can use `requirements.txt` to install necessary packages.

## USAGE:
- Set up the 'InitialURL' variable to point to Web site which you want to generate sitemap for.
- Set script to executable: `sudo chmod +x python-sitemap-generator.py`.
- Run script: `python3 python-sitemap-generator.py`.

![Python Sitemap Generator](https://raw.github.com/wiejakp/python-sitemap-generator/master/screenshot.png)
