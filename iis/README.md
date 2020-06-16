# Inscriptions of Israel/Palestine (IIS) scraper

This is a scraper for the funerary inscriptions (subset) of IIS data.
It makes the second part of a two-part scraping process automatic. 

## Requirements

Note that the IIS module has its own `requirements.txt`. This imports the main requirements file, and adds a single dependency:
'lxml'. This package is notorious for not installing on Windows machines. If you want to use the IIS scraper, please don't have a Windows machine, and go: `pip install -r iis/requirements.txt`.

## Manual part

As you can see, there is a .xml file that should be fed into the scraper.
One was collected at the end of May 2020, but you might want to update it.
IIS let's us connect directly to it SOLR servers, so we have to query for a list of all inscriptions.
First go here:

```
https://library.brown.edu/search/solr_pub/iip/?type=funerary&q=*&fl=inscription_id
```

This will give you only inscription id's, and only the first ten results.
Find the value of `numFound` and do another query to get all inscription id's:

```
https://library.brown.edu/search/solr_pub/iip/?type=funerary&q=*&fl=inscription_id&rows=<whatever_value_you_found>
```

This might take some time. When it's done, copy the reponse and paste it into a file.
This is the file you can feed to the scraper, to scrape individual inscriptions.

## Scraper

This is a very basic scraper. The command line takes two intuitive arguments:

| Option | Alternative form | Required? | Description |
| ------- | ---- | --- | --- |
| 'inscriptions_xml_path' | '-in' | Required | Path of the inscription id xml file. Typically in the input folder of this module. |
| '--export_folder' | '-ef' | Required | Path to the folder where you want the exports to appear. Should be a path to a folder, not a file. |
