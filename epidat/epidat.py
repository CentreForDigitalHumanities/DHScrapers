import os
import logging
from .collectors import EpidatCollector

logger = logging.getLogger(__name__)


def scrape(export_folder):
    '''
    Start by downloading 'howtoharvest' as starting point.
    From that, extract lists of records (i.e. per code, for example 'gda').
    Scrape each record's xml, and enrich it with publication details from the HTML version of the record.
    Immediately print the enriched record to a new file in `export_folder`.

    Keeps track of which lists were fully scraped (i.e. all records from one code) in a file in export folder,
    and will skip the ids present in that list on later subsequent runs.
    '''
    lists_collected_path = os.path.join(export_folder, 'epidat_lists_collected.txt')
    lists_collected = get_lists_collected(lists_collected_path)    
    collector = EpidatCollector()

    try:
        record_list_urls = collector.collect_record_list_urls()
        for index, record_list_url in enumerate(record_list_urls):
            list_id = record_list_url[-3:]
            
            if not list_id + '\n' in lists_collected:
                logger.info('Collecting record list from {} [{}/{}]'.format(
                    record_list_url, index + 1, len(record_list_urls)))
                record_details = collector.collect_record_details(record_list_url)

                for index, detail in enumerate(record_details):
                    if '<' in detail['id']:
                        # if there is html in the record id (and therefore url)
                        # skip because everything will break (i.e. url, filesystem, etc).
                        # This is known to appear in the 'bng' segment, but might appear more often.
                        logger.info('Skipping faulty url \'{}\''.format(detail['url']))
                    else:
                        record_path = os.path.join(export_folder, list_id, detail['id'] + '.xml')
                        if os.path.exists(record_path):
                            logger.info('   Skipping {}'.format(detail['id']))
                        else:
                            logger.info('   Collecting xml for {} from {} [{}/{}]'.format(      
                                detail['id'], detail['url'], index + 1, len(record_details)))
                            record = collector.collect_record(detail)
                            export_record(os.path.join(export_folder, list_id), record, detail)
        
                lists_collected.append(list_id + '\n')
            else:
                logger.info('Skipping {} [{}/{}]'.format(list_id, index + 1, len(record_list_urls)))
    except Exception as e:
        logger.error(e)
    finally:
        save_lists_collected(lists_collected_path, lists_collected)


def get_lists_collected(lists_collected_path):
    lists_collected = []
    if os.path.exists(lists_collected_path):
        with open(lists_collected_path, 'r') as f:
            lists_collected = f.readlines()
    return lists_collected


def save_lists_collected(lists_collected_path, lists_collected):
    with open(lists_collected_path, 'w') as f:
        f.writelines(lists_collected)


def export_record(export_folder, record, record_detail):
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)
    path = os.path.join(export_folder, record_detail['id'] + '.xml')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(record)
