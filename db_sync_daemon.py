#!/usr/bin/env python

import argparse
from db_sync.sync_daemon import SyncDaemon


def parse_args():
    parser = argparse.ArgumentParser(description='Synchronize a Cassandra and an ElasticSearch Report model.')
    parser.add_argument('action', help='start|stop|restart')
    parser.add_argument('--time', help='Database polling time.', default=5)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    action = args.action
    polling_time = int(args.time)

    daemon = SyncDaemon(polling_time, '/tmp/sync_daemon.pid')

    if action == 'start':
        print('Daemon started.')
        print('Logging to /tmp/sync_daemon.log.')
        daemon.start()
    elif action == 'stop':
        daemon.stop()
        print('Daemon stopped.')
    else:
        print('Unkown action.')





