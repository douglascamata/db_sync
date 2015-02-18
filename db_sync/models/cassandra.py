import uuid
from datetime import datetime
from cqlengine import columns
from cqlengine.models import Model
from cqlengine.management import sync_table

class Report(Model):
    uid         = columns.UUID(primary_key=True, default=uuid.uuid4)
    description = columns.Text(required=True)
    created_at  = columns.DateTime(default=datetime.now)

    @classmethod
    def sync_table(cls):
        sync_table(cls)

    @classmethod
    def delete_all(cls):
        all_ids = map(lambda x: str(x.uid), Report.objects.all())
        Report.objects.filter(uid__in=list(all_ids)).delete()

    @classmethod
    def find_by_uid(cls, uid):
        results = [entry for entry in cls.objects(uid=str(uid))]
        return None if len(results) == 0 else results[0]

    def to_dict(self):
        return dict(self)
