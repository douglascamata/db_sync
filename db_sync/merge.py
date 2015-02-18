from db_sync.cassandra import setup_cassandra
from db_sync.elastic_search import setup_elastic_search
from db_sync.models import elastic_search, cassandra
from db_sync.diff import DatabaseDiff


class DatabaseMerger:

    def merge(self, verbose=False):
        if verbose:
            print("Merging databases...")

        self.database_diff = DatabaseDiff().diff()
        self._apply_cassandra_changes()
        self._apply_elastic_search_changes()

        if verbose:
            print("Done.")

    def _apply_cassandra_changes(self):
        self._apply_cassandra_creates()
        self._apply_cassandra_updates()

    def _apply_cassandra_creates(self):
        for item in self.database_diff['cassandra']['create']:
            cassandra.Report.create(uid=item['uid'], description=item['description'])

    def _apply_cassandra_updates(self):
        for item in self.database_diff['cassandra']['update']:
            report = cassandra.Report.find_by_uid(uid=item['uid'])
            report.update(description=item['description'])
            report.save()

    def _apply_elastic_search_changes(self):
        self._apply_elastic_search_creates()
        self._apply_elastic_search_updates()

    def _apply_elastic_search_creates(self):
        for item in self.database_diff['elastic_search']['create']:
            report = elastic_search.Report(uid=str(item['uid']), description=item['description'])
            report.save(refresh=True)

    def _apply_elastic_search_updates(self):
        for item in self.database_diff['elastic_search']['update']:
            report = elastic_search.Report.find_by_uid(str(item['uid']))
            report.description = item['description']
            report.save(refresh=True)
