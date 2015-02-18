#!/usr/bin/env python

import argparse
import asyncio

from db_sync import setup_all
from db_sync.merge import DatabaseMerger


def db_sync(polling_time, loop):
    DatabaseMerger().merge(verbose=True)
    loop.call_later(polling_time, db_sync, polling_time, loop)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Synchronize a Cassandra and an ElasticSearch Report model.')
    parser.add_argument('--time', help='Database polling time.', default=5)
    args = parser.parse_args()

    setup_all()

    loop = asyncio.get_event_loop()
    loop.call_soon(db_sync, int(args.time), loop)

    loop.run_forever()
    loop.close()
