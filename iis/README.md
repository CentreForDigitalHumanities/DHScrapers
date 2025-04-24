# Inscriptions of Israel/Palestine (IIS) scraper

This is a harvesting script for the funerary inscriptions (subset) of IIS data. It harvests data from GitHub, compares versions, and updates as necessary.

The harvested `.xml` files are in the `Epidoc` encoding, which includes information about missing fragments and other deatils. These are not easy to parse for I-Analyzer or other text analysis software, so the app contains a postprocessing step which converts the Epidoc data to a more readable xml format using the [Epidoc XML stylesheets](https://github.com/EpiDoc/Stylesheets).

## Previous version of this scraper
The resources used to be hosted as xml on a website from Brown University. The url of this was not stable, however. At the moment of writing, the inscriptions are available via [a Github repository](https://github.com/Brown-University-Library/iip-texts/), and will be harvested from there.

To refer back to the previous scraper, look at [release 1.0.0](https://github.com/CentreForDigitalHumanities/DHScrapers/releases/tag/1.0.0).

## Requirements
To work with this harvesting script, you need Docker and DockerEngine: this proved to be the easiest way to fully integrate harvesting from GitHub in this repository. As the Docker configuration is using named volumes, the harvested data will persist.

## Scraper

This is a very basic scraper. The command line takes two intuitive arguments:

| Option | Alternative form | Required? | Description |
| ------- | ---- | --- | --- |
| 'inscriptions_xml_path' | '-in' | Required | Path of the inscription id xml file. Typically in the input folder of this module. |
| '--export_folder' | '-ef' | Required | Path to the folder where you want the exports to appear. Should be a path to a folder, not a file. |
