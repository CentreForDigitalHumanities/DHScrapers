'''
This is a standalone script, that helps you extract some details
about the inscriptions for which scraping failed from the log file
created by the scraper.
'''

import requests
import os

for directory, _, filenames in os.walk('./output/epidat'):
    for filename in filenames:
        name, extension = os.path.splitext(filename)
        full_path = os.path.join(directory, filename)

        with open(full_path, 'r') as f_in:
            text = f_in.read()
            if 'XML not valid' in text:
                os.remove(full_path)
            elif 'File can not be displayed, because date of burial is later than 1950' in text:
                os.remove(full_path)
