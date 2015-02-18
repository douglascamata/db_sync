import unittest2 as unittest
import uuid
from datetime import datetime

from db_sync.models import elastic_search, cassandra
from db_sync.elastic_search import setup_elastic_search
from db_sync.cassandra import setup_cassandra
from db_sync.diff import DatabaseDiff

class TestDiff(unittest.TestCase):

    def setUp(self):
        setup_elastic_search()
        setup_cassandra()

        cassandra.Report.sync_table()
        elastic_search.Report.sync_index()

    def tearDown(self):
        cassandra.Report.delete_all()
        elastic_search.Report.delete_all()

    def testSameRecords(self):
        uid = str(uuid.uuid4())
        now = datetime.fromtimestamp(1424285183.0)

        first_report = cassandra.Report.create(uid=uid, description='My very first cassandra report', created_at=now)
        second_report = elastic_search.Report(uid=uid, description='My very first elastic search report', created_at=now)
        second_report.save(refresh=True)

        diff = DatabaseDiff().diff()

        result_dict = {
            'cassandra': {
                'create': [],
                'update': []
            },
            'elastic_search': {
                'create': [],
                'update': []
            }
        }

        self.assertEquals(diff, result_dict)

    def testCassandraHasMoreRecords(self):
        uid = uuid.uuid4()
        first_report = cassandra.Report.create(uid=uid, description='My very first report')

        diff = DatabaseDiff().diff()
        self.assertEquals(len(diff['elastic_search']['create']), 1)

    def testElasticSearchHasMoreRecords(self):
        uid = str(uuid.uuid4())
        report = elastic_search.Report(uid=uid, description='My very first report')
        report.save(refresh=True)

        diff = DatabaseDiff().diff()
        self.assertEquals(len(diff['cassandra']['create']), 1)

    def testBothHaveNewRecords(self):
        first_report = cassandra.Report.create(description='My very first report')
        second_report = elastic_search.Report(description='My very first report')
        second_report.save(refresh=True)

        diff = DatabaseDiff().diff()

        self.assertEquals(len(diff['cassandra']['create']), 1)
        self.assertEquals(len(diff['elastic_search']['create']), 1)

    def testCassandraHasOlderRecord(self):
        uid = str(uuid.uuid4())
        second_report = elastic_search.Report(uid=uid, description='My very first report')
        second_report.save(refresh=True)
        first_report = cassandra.Report.create(uid=uid, description='My very first report')

        diff = DatabaseDiff().diff()

        self.assertEquals(len(diff['cassandra']['create']), 0)
        self.assertEquals(len(diff['cassandra']['update']), 0)
        self.assertEquals(len(diff['elastic_search']['create']), 0)
        self.assertEquals(len(diff['elastic_search']['update']), 1)

    def testElasticSearchHasOlderRecord(self):
        uid = str(uuid.uuid4())
        first_report = cassandra.Report.create(uid=uid, description='My very first report')

        second_report = elastic_search.Report(uid=uid, description='My very first report')
        second_report.save(refresh=True)

        diff = DatabaseDiff().diff()

        self.assertEquals(len(diff['cassandra']['create']), 0)
        self.assertEquals(len(diff['cassandra']['update']), 1)
        self.assertEquals(len(diff['elastic_search']['create']), 0)
        self.assertEquals(len(diff['elastic_search']['update']), 0)


if __name__ == '__main__':
    unittest.main()
