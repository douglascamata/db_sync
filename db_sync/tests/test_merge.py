import unittest2 as unittest
import uuid
from db_sync.models import elastic_search, cassandra
from db_sync.elastic_search import setup_elastic_search
from db_sync.cassandra import setup_cassandra
from db_sync.merge import DatabaseMerger


class TestMerge(unittest.TestCase):

    def setUp(self):
        setup_elastic_search()
        setup_cassandra()

        cassandra.Report.sync_table()
        elastic_search.Report.sync_index()

    def tearDown(self):
        cassandra.Report.delete_all()
        elastic_search.Report.delete_all()

    # Cassandra tests
    def test_create_one_in_cassandra(self):
        uid = str(uuid.uuid4())

        second_report = elastic_search.Report(uid=uid, description='My very first report')
        second_report.save(refresh=True)

        merger = DatabaseMerger()
        merger.merge()

        first_report = cassandra.Report.find_by_uid(uid=uid)
        self.assertEqual(first_report.description, second_report.description)

    def test_update_one_in_cassandra(self):
        uid = str(uuid.uuid4())

        first_report = cassandra.Report(uid=uid, description='foo')

        second_report = elastic_search.Report(uid=uid, description='My very first report')
        second_report.save(refresh=True)

        merger = DatabaseMerger()
        merger.merge()

        first_report = cassandra.Report.find_by_uid(uid=uid)
        self.assertEqual(first_report.description, second_report.description)

    def test_update_and_create_in_cassandra(self):
        uid = str(uuid.uuid4())

        first_report = cassandra.Report(uid=uid, description='ex-cassandra')

        second_report = elastic_search.Report(uid=uid, description='Elastic')
        second_report.save(refresh=True)

        third_report = elastic_search.Report(description='Elastic')
        third_report.save(refresh=True)

        merger = DatabaseMerger()
        merger.merge()

        first_report = cassandra.Report.find_by_uid(uid=uid)
        third_report_in_cassandra = cassandra.Report.find_by_uid(uid=third_report.uid)
        self.assertEqual(first_report.description, second_report.description)
        self.assertEqual(third_report_in_cassandra.description, third_report.description)

    # Elastic Search tests
    def test_create_one_in_elastic_search(self):
        uid = str(uuid.uuid4())

        second_report = cassandra.Report.create(uid=uid, description='My very first report')

        merger = DatabaseMerger()
        merger.merge()

        first_report = elastic_search.Report.find_by_uid(uid=uid)
        self.assertEqual(first_report.description, second_report.description)

    def test_update_one_in_elastic_search(self):
        uid = str(uuid.uuid4())

        first_report = elastic_search.Report(uid=uid, description='foo')
        first_report.save(refresh=True)

        second_report = cassandra.Report.create(uid=uid, description='My very first report')

        merger = DatabaseMerger()
        merger.merge()

        first_report = elastic_search.Report.find_by_uid(uid=uid)
        self.assertEqual(first_report.description, second_report.description)

    def test_update_and_create_in_elastic_search(self):
        uid = str(uuid.uuid4())

        first_report = elastic_search.Report(uid=uid, description='ex-cassandra')
        first_report.save(refresh=True)

        second_report = cassandra.Report.create(uid=uid, description='Elastic')

        third_report = cassandra.Report.create(description='Elastic')

        merger = DatabaseMerger()
        merger.merge()

        first_report = elastic_search.Report.find_by_uid(uid=uid)
        third_report_in_elastic = elastic_search.Report.find_by_uid(uid=third_report.uid)
        self.assertEqual(first_report.description, second_report.description)
        self.assertEqual(third_report_in_elastic.description, third_report.description)



if __name__ == '__main__':
    unittest.main()
