import asyncio
from proxy import logger
from contextlib import closing
from http_parser.parser import HttpParser

class Server():
    @staticmethod
    def parse_http(data):
        parser = HttpParser()
        parser.execute(data, len(data))
        has_connect = parser.get_method() == 'CONNECT'
        print(parser.get_method())
        dest_port = 80
        if has_connect:
            dest_addr = parser.get_url()
        else:
            dest_addr = parser.get_headers()['Host']

        if ':' in dest_addr:
            dest_addr, port = dest_addr.split(':')
            dest_port = int(port)

        return has_connect, dest_addr, dest_port

    @staticmethod
    async def pipe_data(src_reader, src_writer, dest_reader, dest_writer):
        async def pipe(reader, writer, closed):
            while not closed.is_set():
                data = await reader.read(4096)
                if not data:
                    closed.set()
                    break
                writer.write(data)
                await writer.drain()

        closed = asyncio.Event()
        await asyncio.gather(pipe(src_reader, dest_writer, closed),
                             pipe(dest_reader, src_writer, closed))

    @staticmethod
    async def handle_conn(src_reader, src_writer):
        src_host, src_port = src_writer.get_extra_info('peername')

        try:
            data = await src_reader.readuntil(b'\r\n\r\n')
            has_connect, dest_addr, dest_port = Server.parse_http(data)
        except (BaseException):
            src_writer.close()
            logger.debug(f"Closed connection to {src_host}:{src_port}, incorect HTTP request")
            return
        with closing(src_writer):
            logger.debug(f"Received from {src_host}:{src_port}:\n{data.decode()}")
            logger.debug(f"Openning connection to {dest_addr}:{dest_port}")
            dest_reader, dest_writer = await asyncio.open_connection(dest_addr, dest_port)
            with closing(dest_writer):
                if has_connect:
                    src_writer.write(b'HTTP/1.1 200 OK\r\n\r\n')
                    await src_writer.drain()
                else:
                    dest_writer.write(data)
                    await dest_writer.drain()
                await Server.pipe_data(src_reader, src_writer, dest_reader, dest_writer)
            logger.debug(f"Closed connection to {dest_addr}:{dest_port}")

    def __init__(self, host, port):
        self.host = host
        self.port = port
        logger.setup_logger(__name__)


    async def start_impl(self):
        server = await asyncio.start_server(Server.handle_conn, self.host, self.port)
        logger.info(f'Server started on: {self.host}:{self.port}')

        async with server:
            await server.serve_forever()

    def start(self):
        asyncio.run(self.start_impl())
