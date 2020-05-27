import logging

def init_logger(log_file='scrape.log'):
    '''
    Initialize a logger that will log INFO (and above) to the console,
    and DEBUG and above a file.

    Parameters:
        log_file -- name of the log file, defaults to scrape.log
    '''
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(log_file)
    fh_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(fh_formatter)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch_formatter = logging.Formatter('%(asctime)s - %(message)s')
    ch.setFormatter(ch_formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)

    logging.getLogger("dicttoxml").setLevel(logging.WARNING)