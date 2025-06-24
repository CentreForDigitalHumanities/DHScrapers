# Inscriptions of Israel/Palestine (IIS) scraper

This is a harvesting script for the funerary inscriptions (subset) of IIS data. It harvests data from GitHub, compares versions, and updates as necessary.

The harvested `.xml` files are in the `Epidoc` encoding, which includes information about missing fragments and other deatils. These are not easy to parse for I-Analyzer or other text analysis software, so the app contains a postprocessing step which converts the Epidoc data to a more readable xml format using the [Epidoc XML stylesheets](https://github.com/EpiDoc/Stylesheets).

## Previous version of this scraper
The resources used to be hosted as xml on a website from Brown University. The url of this was not stable, however. At the moment of writing, the inscriptions are available via [a Github repository](https://github.com/Brown-University-Library/iip-texts/), and will be harvested from there.

To refer back to the previous scraper, look at [release 1.0.0](https://github.com/CentreForDigitalHumanities/DHScrapers/releases/tag/1.0.0).

## Requirements
To work with this harvesting script, you need Docker and DockerEngine: this proved to be the easiest way to fully integrate harvesting from GitHub in this repository. As the Docker configuration is using named volumes, the harvested data will persist.

## Scraper
### Locally
To scrape locally, use the [docker-compose-iis file](https://github.com/CentreForDigitalHumanities/DHScrapers/blob/a59ffe8d21612d2aa130889b667a62b0faf6dc71/docker-compose-iis.yaml) in the base path of this repository. `docker-compose -f docker-compose-iis.yaml up` will do the following:
- iis-harvest:
    - pulls the image [dh-scrapers-iis](https://github.com/CentreForDigitalHumanities/DHScrapers/pkgs/container/dh-scrapers-iis), and checks the contents of the directory mounted from `./volumes/iis-files/originals` against the Brown University GitHub repository, and pulls in changed files in the `epidoc-files` subdirectory. The changed files will also be written to a `inprogress.txt` file on a shared volume (mounted from `./volumes/iis-metadata`)
    - if the file `inprogress.txt` is already present, the harvester skips the above step.
    - the `dh-scrapers-iis` image also contains `epidoc` stylesheets, which are copied to a shared volume (mounted from `./volumes/epidoc-stylesheets`). These are needed to process the `xml` format of the inscriptions, which include rich information about illegible or missing fragments, into plaintext.
- iis-parse:
    - the script in `iis/collect.py` walks over the files in the `inprogress.txt` file and enriches them with bibliographical information via Zotero. The parsed files will be in `./volumes/iis-output/`.
    - should the parse process be interrupted, the parser will skip files existing in `./volumes/iis-output`.
    - once the parse process is complete, the `inprogress.txt` document will be renamed to a `{timestamp}.txt` file, so that the next time `git diff` is run, it goes to a fresh `inprogress.txt` file.
- iis-prepare-postprocess:
    - checks which of the parsed files have already been postprocessed by comparing the contents of the volumes mounted at `./volumes/iis-output` and `./volumes/iis-postprocessed`.
    - the postprocessed files will be moved to a subdirectory, `./volumes/iis-output/{timestamp}`. This is done to avoid postprocessing multiple times, as postprocessing is by far the most time-intensitive step of the pipeline.
- iis-postprocess:
    - uses a third-party image for Saxon to convert the `xml` files with the xml stylesheets downloaded by the `iis-harvest` step.
- iis-index:
    - uses the `ghcr.io/centrefordigitalhumanities/ianalyzer-backend-dependencies:latest` image to index to Elasticsearch. The Elasticsearch settings come from the `./settings/iis_settings` file.

### For production
The pipeline described above has also been implemented through Kubernetes. The manifests can be found in `./kmanifests/`. The manifests set up a persistent volume, and the config map for non-sensitive information.

The Kubernetes job is triggered through the [dh-scrapers-flow](https://github.com/CentreForDigitalHumanities/DHScrapers/blob/a59ffe8d21612d2aa130889b667a62b0faf6dc71/.github/workflows/dh-scrapers-flow.yaml) GitHub action.

Refer to the [kmanifests README](https://github.com/CentreForDigitalHumanities/DHScrapers/blob/a59ffe8d21612d2aa130889b667a62b0faf6dc71/.github/workflows/dh-scrapers-flow.yaml) for more information.
