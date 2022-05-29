from proxy import logger
from proxy import server

def start():
    logger.setup_logger(__name__)
    logger.info('Proxy server started')
    s = server.Server('localhost', 1234)
    s.start()
