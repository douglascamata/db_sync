import unittest2 as unittest
import uuid
from db_sync.models.elastic_search import Report
from db_sync.elastic_search import setup_elastic_search


class TestElasticSearchModel(unittest.TestCase):

    def setUp(self):
        setup_elastic_search()
        Report.sync_index()

    def tearDown(self):
        Report.delete_all()

    def test_report_creation(self):
        report = Report(description='My very first report')
        report.save(refresh=True)
        self.assertEqual(report.description, 'My very first report')
        self.assertEqual(len(Report.search().execute().hits), 1)

    def test_elastic_search_model_dict(self):
        report = Report(description='Test as dict')
        result = report.to_dict()
        self.assertEqual(result['description'], 'Test as dict')

    def test_find_by_uid(self):
        uid = str(uuid.uuid4())
        report = Report(uid=uid, description='Anything')
        report.save(refresh=True)

        report = Report.find_by_uid(uid)
        self.assertTrue(report)



if __name__ == '__main__':
    unittest.main()
