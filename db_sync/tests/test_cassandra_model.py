import uuid
import unittest2 as unittest
from db_sync.models.cassandra import Report
from db_sync.cassandra import setup_cassandra

class TestCassandraModel(unittest.TestCase):

    def setUp(self):
        setup_cassandra()
        Report.sync_table()

    def tearDown(self):
        Report.delete_all()

    def test_report_creation(self):
        report = Report.create(description='My very first report')
        self.assertEqual(report.description, 'My very first report')
        self.assertEqual(Report.objects.count(), 1)
        self.assertTrue(report.created_at)

    def test_report_as_dict(self):
        report = Report.create(description='My very first report')
        as_dict = report.to_dict()
        self.assertTrue(isinstance(as_dict, dict))
        self.assertEqual(as_dict['description'], 'My very first report')

    def test_find_by_uid(self):
        uid = str(uuid.uuid4())
        report = Report.create(uid=uid, description='My very first report')

        report = Report.find_by_uid(uid)
        self.assertTrue(report)

if __name__ == '__main__':
    unittest.main()
