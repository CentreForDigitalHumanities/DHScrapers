# Epidat scraper

This is a scraper for the [Epidat](http://www.steinheim-institut.de/cgi-bin/epidat) corpus of Jewish inscriptions. It works on the basis of a list of available records provided by epidat itself, right [here](http://www.steinheim-institut.de/cgi-bin/epidat?info=howtoharvest). It will collect this list, and one by one will collect the XML version of each record, AND it will enrich this data with publication details collected from the HTML version of the same record.

Note that the epidat corpus is grouped based on a (geographically based) code, e.g. `aha` (Ahaus), `bme` (Bad Münstereifel), etc. This structure is kept: each group ends up in its own folder.

## Scraping

Getting the scraper in action is easy as pie. There is only one parameter: `--export_folder`, i.e. the folder where you need the results to end up.

However, when scraping the corpus in June 2020, the epidat server didn't always respond as friendly, i.e. the scraper grinded to a halt every few hours. Therefore, the scraper keeps track of which 'groups' (see above) were already completed in a file in `export_folder`. You don't have to do anything with this, but when scraping you could use to exclude or skip particular groups. For completeness sake, an example of this file is included (`example_lists_collected.txt`), that includes all groups: this might be useful if a partial (re)scrape has to be performed.

## `epidat_post_processor.py`

The files collected will contain two types of files that you probably do not want in your data, those with

1) a `body` that contains only the message that the XML is not valid. This occured 135 times  in June 2020 (out of 35502 total).

2) a `body` that contains the message that the 'File can not be displayed, because date of burial is later than 1950'. This occured 954 times in June 2020 (out of 35502 total)

You can remove those records by running `epidat_post_processor.py`.
