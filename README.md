# Python Sitemap Generator

- Version: 0.5
- Update: 2023/04/22

Python Site Map Generator uses python multi-threaded approach to read all links accessible through the Web site and generate proper sitemap for SEO purposes. In this redesigned version non-ascii urls are supported. 
Script was meant to use threading technology to allow easy and very fast approach while generating sitemaps for your Web pages.
The script will run under Linux operating system which supports Python 3 language.

Use with caution, if you set thread count too high, it can cause your web server to bug out and cause some links to throw an error, or your IP will be blocked due to firewall threashold.

## REQUIREMENTS
The code is updated to newer version which supports `python 3.9`. Now you can use `requirements.txt` to install necessary packages. Required packages are:
- lxml
- bs4
- beautifulsoup4
- var_dump

## USAGE:
Now, for use the Site Map Generator you can easily use CLI:

```commandline
python sitemap_generator.py -u example.com -mt 4 -f sitemap.xml
```

**CLI help:**

```commandline
usage: sitemap_generator.py [-h] -u URL [-f FILENAME] [-mt MAX_THREADS] [-d DUMP]

A python Site Map Generator, that crawl any webpage and generate XML sitemap compatible with Google's indexing robot.

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL
  -f FILENAME, --filename FILENAME
  -mt MAX_THREADS, --max-threads MAX_THREADS
  -d DUMP, --dump DUMP  To show html of pages in console. To enable set it to 1. The default is -1.
```

**Sample Response:**

```commandline
Threads:  1  Queue:  0  Checked:  0  Link Threads:  1
Threads:  1  Queue:  0  Checked:  0  Link Threads:  1
Threads:  1  Queue:  0  Checked:  0  Link Threads:  1
Threads:  1  Queue:  0  Checked:  0  Link Threads:  1
Threads:  1  Queue:  0  Checked:  0  Link Threads:  1
Checked:  1
Running XML Generator...
Sitemap saved in:  sitemap.xml
Elapsed Time: 5.008033752441406
```
