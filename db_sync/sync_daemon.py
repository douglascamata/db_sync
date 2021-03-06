import asyncio
import logging
from db_sync.utils.daemon import daemon
from db_sync import setup_all
from db_sync.merge import DatabaseMerger


class SyncDaemon(daemon):

    def __init__(self, polling_time, pidfile):
        self.polling_time = polling_time
        super().__init__(pidfile)

    def run(self):
        self.setup_logging()
        main(self.polling_time)

    def setup_logging(self):
        logger = logging.getLogger('SyncDaemon')
        logger.setLevel(logging.DEBUG)

        fh = logging.FileHandler('/tmp/sync_daemon.log')
        fh.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        fh.setFormatter(formatter)
        logger.addHandler(fh)


def main(polling_time):
    setup_all()

    loop = asyncio.get_event_loop()
    loop.call_soon(db_sync, polling_time, loop)
    loop.run_forever()
    loop.close()

def db_sync(polling_time, loop):
    DatabaseMerger().merge(verbose=True)
    loop.call_later(polling_time, db_sync, polling_time, loop)
