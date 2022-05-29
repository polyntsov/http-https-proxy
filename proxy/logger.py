import logging

def setup_logger(name):
    # create logger
    global Logger
    Logger = logging.getLogger(name)
    Logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - [%(levelname)s]: %(message)s',
                                  datefmt='%d.%m.%Y %H:%M:%S')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    Logger.addHandler(ch)

def info(msg):
    Logger.info(msg)

def debug(msg):
    Logger.debug(msg)
