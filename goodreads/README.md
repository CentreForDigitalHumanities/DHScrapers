# GoodReads scraper(s)

Our scrapers are basically some scripts that work together to extract as many reviews for a title as possible from GoodReads.com. Our solution to GoodReads' limitations (e.g. 300 reviews per title per language -- at least at first sight), combines the option to filter per rating with the option to filter reviews only for the edition currently viewed. Reviews are extracted per edition, and if more than 300 are found for the current edition, these are collected _per rating_. This means that a potential 1500 reviews are extracted for each edition! (Well, as long as that number of reviews exists for the edition of course.)

## Introduction

The GoodReads scraper actually consists of two scrapers. The main entry point to the module (the script `goodreads.py`) combines these into one action. As explained above, our scraper feeds off the fact that on GoodReads, a title exists in several editions. The first scraper collects all the editions for a title, while the second one collects as many reviews as possible for each editions. The output is always exported as a `.csv`) file, and can additionally be exported as `XML` and `TXT`.

### Edition scraper

The starting point of each sraping session will be a list of editions for a title. This list can be found by clicking 'All Editions' (just above the tiny pictures of the other editions).

![ss_title](https://user-images.githubusercontent.com/30618796/79224990-55cfe380-7e5c-11ea-8460-ec27528b8900.png)

The edition scraper extracts the following details for each edition. Note that you can export these (too, i.e. in addition to the reviews) if you want, see below.

| property | description |
| ---- | ---- |
| title |
| url | GoodsReads url for the edition
| authors | a comma-separated list of the authors, incl role. Example: 'Herman Koch,Sam Garrett (Translator)'
| pub_details | Example: 'Published 2013 by Atlantic Books'
| edition_details | Example: 'Paperback, 309 pages'
| isbn |
| isbn13 |
| asin |
| language | The language of the edition
| avg_rating | Average rating for the edition
| number_of_ratings | Total number of ratings for the edition

### Review scraper

The main thing these scripts do, is extract reviews. Note that there is a difference on GoodReads between reviews and ratings. Reviews have actual text, whereas a rating is just a score from 1 to 5. A rating does not require text, **and vice versa**, i.e. a review does not always imply that a rating is present. The scraper is interested in reviews only, and will ignore all 'reviews' that are rating-only.

Interestingly, the reviews that one sees on any title's page are supplied to the GoodReads website by an API / webservice that returns a bunch of HTML and Javascript to be displayed in the page (i.e. a sort of subpage). The review scraper addresses this API directy, bypassing the website entirely.

Upon collecting the first page of reviews, the review scraper establishes how many reviews exist for the current edition. If this is more than 300 (i.e. a Top 300 is presented), it will collect on a _per rating_ basis, i.e. it will first collect up to 300 reviews with rating 1, then rating 2, etc. If less than 300 reviews for a rating exist, it simply collects whatever number of reviews is available. (Note that this is non-trivial because GoodReads filtering system can respond with surprising results. More about this in the 'For Developers' section.)

A review looks like this:

| property | description |
| ---- | ---- |
| id | The GoodReads id for the review |
| url | GoodReads url for the review |
| edition_id | The GoodReads id for the edition the review belongs to
| edition_language | Language of the edition the review belongs to, as a full word (e.g. 'English') |
| edition_publisher | Publisher of the edition the review was written for |
| edition_publishing_year | Year of publication of the edition the review was written for |
| date | Date the review was published on GoodReads |
| author | User that wrote the review |
| author_gender | The gender of the author. (Note that this is detected by the scraper, see below) |
| language | The language the review is written in. (Note that this is detected by the scraper, see below) |
| rating | The rating that comes with the review. Isn't typically, but can be empty. |
| text | The full text of the review |

#### Language Detection

In its current form, the review scraper tries to establish the language of a review using the [langdetect](https://pypi.org/project/langdetect/) package. Be aware that this works really great for most reviews, but not those that consist of just one or two words. Just sayin'.

Also note that a `langdetect` returns language _codes_ ('nl'), so an addtional package [iso-639](https://pypi.org/project/iso-639/) is used to translate these into language _names_ ('Dutch').

#### Gender guessing

The scraper uses [gender-guesser](https://pypi.org/project/gender-guesser/) to guess an authors gender based on their username. (Note that first result do not look that promising, probably due to the use of username).

### goodreads.py

The main entry point, the script that makes life easy for the user by combining the two scrapers into one simple command. The options:

| Option | Alternative form | Required? | Description |
| ------- | ---- | --- | --- |
| '--editions_url' | '--url', '-eu' | Required | The url of an editions page. May or may not include the page queryparam at the end. You can find the url by clicking 'All Editions' (under Other Editions') on a title's page. Just copy and paste from your browser's address bar. Example: `https://www.goodreads.com/work/editions/6463092-het-diner`. |
| '--export_folder' | '-ef' | Required | Path to the folder where you want the exports to appear. Should be a path to a folder, not a file. |
| '--reviews_export_csv_filename' | '-ref' | Optional | Filename for the csv you want to the reviews exported to. Should be a .csv file. Defaults to 'reviews.csv' |
| '--editions_export_csv_filename' | '-eef' | Optional | Filename for the csv you want the editions exported to.
                Should be a .csv file. Editions will not be exported to csv if you leave this empty |
| '--xml' | '--export_xml' | Optional | If this flag is present (no value needed), each review is exported to an XML file |
| '--txt' | '--export_txt' | Optional | | If this flag is present (no value needed), each review is exported to a txt file |
| '--edition_languages' | '-el' | Optional | Choose one or multiple from 'English', 'German', 'Dutch', 'French', 'Spanish' or 'all'. Example: `-el English German`. Defaults to 'all'.

Example: `python -m goodreads --editions_url "https://www.goodreads.com/work/editions/6463092-het-diner" -ef ./TheDinner -el English Dutch --xml`

IMPORTANT: it has occured, especially when scraping reviews for a large number of editions, that the GoodReads server takes too long to respond. If this happens, the scraping crashes. The best we currently have to offer is to simply start over: we have succesfully scraped over 17000 reviews from 356 editions of _Harry Potter and the Sorcerer's Stone_.

## For developers

### Filtering reviews

In the above, we've hinted a couple of times at the unpredictabe nature of GoodReads review filtering system. There is actually a logic to it, that we'll document here for future reference.

All filtering is done by supplying query parameters to the reviews API discussed above. There are a number of options:

| Parameter | Type | Description |
| ---- | ---- | ---- |
| language_code | String | Filter reviews per language. If this is supplied, all other queryparams are ignored |
| edition_reviews | Boolean | Filter reviews to include only those for the current edition (or not) |
| rating | number between 1 and 5 | Filter per rating |
| text_only | Boolean | Filter reviews to include only those with text. Will lead to surprising results, see below. |
| page | number (up to 10) | The number of the page with results. 30 results per page |

#### text_only

The `text_only` param leads to surprising results in some cases, especially in different combinations with `edition_reviews`  and `rating`. One would expect to be able to filter for all reviews of this edition with rating 5 that actually have text. While such a query produces the correct number for the amount of text-only reviews for this edition and rating in the 'Displaying X from Y' element, on the pages there could still be ratings included, sometimes in combination with reviews _with a different rating_.

For example, consider this query: `https://www.goodreads.com/book/reviews/22561799-het-diner?edition_reviews=true&text_only=true`. This displays, according to itself, results '1-7 of 2 text-only reviews for this edition'. Say whaaaat?? It turns out the results consist of 2 reviews with text and 5 ratings. This happens because there are no more results for this particular edition.

Even more interesting is when no reviews(-with-text) of a particular rating exist, and only a small number of ratings is found. Think about `https://www.goodreads.com/book/reviews/28550610-harry-potter-and-the-sorcerer-s-stone?edition_reviews=true&text_only=true&rating=2`. This will return a page with 30 reviews, a mix of ratings and reviews(-with-text). However, upon closer inspection, it turns out there is only 1 actual rating of 2 stars (the first result), which is then supplemented with ratings and reviews _with totally different scores_(!).

The reviews scraper can handle all these cases, and should never extract any reviews that do not fit the actual query, regardless of the results in the response. Keep that in mind during future development.

Note that these different outcomes of the mentioned queries can be found in the 'testdata' folder of the review_scraper, including more details on what exactly is in these files in `testdata_details.md`.
