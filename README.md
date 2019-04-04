# crawler_company_profiles
This app created using Python with Scrapy framework.

This app crawling data with source url taken from company_index.json and created in special purpose for crawling data from urls provided on the file. There are about 3300s list of urls, and the download_delay configured at 5 s.

## Prerequisite
Install python on your machine. You can use [python](https://www.python.org/) or [anaconda](https://www.anaconda.com/).

Install scrapy:
```bash
#if using pip:
pip install Scrapy

#if using anaconda
conda install -c conda-forge scrapy
#or
conda install -c conda-forge/label/cf201901 scrapy
```

## Usage
Firstly download or clone this repo.

### Download Delay
We need to be nice to any site, which we wanted to crawl, by setting a download delay in settings.py:

```python
DOWNLOAD_DELAY = 5

```

### Crawl
On your command line:
```bash
scrapy crawl sgmarine_profiles -o company_profiles.json -t json
```

#### Explanation:

The "sgmarine_profiles" is name of this crawler. you can change this name on /spiders/stack_spyder.py, in class StackSpider.
```python
...
  name = "sgmarine_profiles"
  ...
```

The "company_profiles.json" is the output file name. You can change file format to other like a csv by change this part "-t json" to "-t csv"


#### Result:
The running time is depend on your "download_delay" setting, if it is set for 1s so it will be about 3300s running time (for 3300s url).
