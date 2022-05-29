from proxy import logger
from proxy import server

def start(host, ip):
    logger.setup_logger(__name__)
    logger.info('Proxy server started')
    s = server.Server(host, ip)
    s.start()
