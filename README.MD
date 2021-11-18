# Test task for interview
 1. Scrape the below mentioned website for all the Cars and their Details 
https://www.tred.com/buy?body_style=&distance=50&exterior_color_id=&make=&miles_max=100000&miles_min=0&model=&page_size=24&price_max=100000&price_min=0&query=&requestingPage=buy&sort=desc&sort_field=updated&status=active&year_end=2022&year_start=1998&zip=
 2. The script should be written in a way that user can input a zipcode and radius which will be entered in corresponding fields. You may use Selenium to accomplish this. 
 3. After going into each of the results that show up, some attributes should be scrapped. The list of attributes to be scrapped is given below for your reference:
    - Name
    - Price
    - Vehicle Summary
    - Options
 4. The output of the web scrapper should be fed into an Excel Workbook (.xlsx file) where each of these attributes are written in separate columns.

# Installation
 - Install requirements: `pip install -r requirements.txt`
 - Download webdriver and put it into `./drivers` directory
 - Written on Python 3.9
 
## Setting up

Before starting is needed to set CLI parameters:
```
usage: start.py [-h] [--url URL] -z ZIP_CODE -r RADIUS [-w MAX_WORKERS] [-spw SELENIUM_PROCESSOR_MAX_WORKERS] [-o OUTPUT_FILENAME] [--collector {selenium}] [--processor {api,selenium}]
                [--writer {excel}]

Tool for collecting data

optional arguments:
  -h, --help            show this help message and exit
  --url URL             Site URL for collecting
  -z ZIP_CODE, --zip_code ZIP_CODE
                        Zip code for collecting
  -r RADIUS, --radius RADIUS
                        Radius for collecting
  -w MAX_WORKERS, --max_workers MAX_WORKERS
                        Max workers for simultaneous collecting
  -o OUTPUT_FILENAME, --output_filename OUTPUT_FILENAME
                        Filename for output data
  --collector {selenium}
                        Collector type
  --processor {api,selenium}
                        Processor type
  --writer {excel}      Writer type
```

# Launching

There are 2 main types of launching:

1. `python start.py --zip_code 98052 --radius 25 --processor api --max_workers 10`

    Launch collector (one browser window) and processor that pulls data through API.
    Then processor adding data to results in 'manual' way - it means that data returned with API requests
    is processed in strictly specified way.

    **Pros**: fast, have some data that are not displaying on the page

    **Cons**: resulting data is depends on specified way of data processing: not all data from the page may be added to result

    **Test results**: `url='https://www.tred.com', zip_code='98052', radius='25', max_workers=30, output_filename='output.xlsx', collector='selenium', processor='api', writer='excel'`

    Elapsed: ~25 seconds

2. `python start.py --zip_code 98052 --radius 25 --processor selenium --max_workers 10`

    Launch collector (one browser window) and processor that pulls data from pages directly.
    Processor has many browser windows and simultaneously pulls data from many pages.
    Processor's windows do not close after receiving a portion of data: the same windows is used for getting other data units.

    **Pros**: data is received directly from page and added to results exactly the same composition as on the page.

    **Cons**: much slower than using API, cannot get data that are not displaying on the page

    **Test results**: `url='https://www.tred.com', zip_code='98052', radius='25', max_workers=10, output_filename='output.xlsx', collector='selenium', processor='selenium', writer='excel'`

    Elapsed: ~250 seconds

