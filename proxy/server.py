import socket
import asyncio
from proxy import logger

class Server():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        logger.setup_logger(__name__)

    @staticmethod
    async def handle_conn(reader, writer):
        peer_host, peer_port = writer.get_extra_info('peername')
        while True:
            try:
                data = await reader.readuntil(b'\r\n\r\n')
            except (asyncio.IncompleteReadError):
                writer.close()
                logger.debug(f"Closed connection with {peer_host}:{peer_port}")
                break

            message = data.decode()
            logger.debug(f"Received {message!r} from {peer_host}:{peer_port}")

    async def start_impl(self):
        server = await asyncio.start_server(Server.handle_conn, self.host, self.port)
        logger.info(f'Server started on: {self.host}:{self.port}')

        async with server:
            await server.serve_forever()

    def start(self):
        asyncio.run(self.start_impl())
