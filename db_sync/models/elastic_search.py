import uuid
from datetime import datetime
from elasticsearch_dsl import DocType, String, Date, Integer


class Report(DocType):
    uid = String()
    description = String(analyzer='snowball', fields={'raw': String(index='not_analyzed')})
    created_at = Date()

    class Meta:
        index = 'report'

    def __init__(self, **kwargs):
        if not 'uid' in kwargs:
            kwargs['uid'] = str(uuid.uuid4())
        if not 'created_at' in kwargs:
            kwargs['created_at'] = datetime.now()
        return super().__init__(**kwargs)

    def to_dict(self):
        super_result = super(DocType, self).to_dict()
        return super_result

    @classmethod
    def sync_index(cls):
        cls.init()

    @classmethod
    def find_by_uid(cls, uid):
        result = cls.search().query('match', uid=str(uid)).execute().hits
        return None if len(result) == 0 else result[0]

    @classmethod
    def delete_all(cls):
        for item in Report.search().execute():
            item.delete(refresh=True)
