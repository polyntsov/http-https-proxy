from proxy import proxy
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="HTTP/HTTPS proxy")
    parser.add_argument("host", type=str, help="ip address to run server on")
    parser.add_argument("port", type=int, help="port to run server on")
    return parser.parse_args()

args = parse_args()

proxy.start(args.host, args.port)
