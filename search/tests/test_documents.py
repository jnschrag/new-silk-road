from django.test import TestCase, override_settings
import os
from elasticsearch_dsl import Search
from elasticsearch_dsl.connections import connections
from writings.tests.factories import EntryFactory
from search.mappings import EntryMapping
from search.documents import EntryDoc
from search.utils import create_search_index


TEST_SEARCH = {
    'default': {
        'index': 'test_reconnectingasia',
        'connections': {
            'hosts': [os.getenv('ELASTICSEARCH_TEST_URL', 'http://localhost:9200')],
            'timeout': 20,
        }
    }
}


@override_settings(SEARCH=TEST_SEARCH)
class DocumentsTestCase(TestCase):

    def setUp(self):
        connections.create_connection('testing', **TEST_SEARCH['default']['connections'])
        self.index = create_search_index(TEST_SEARCH['default']['index'], (EntryDoc,), connection='testing')
        if self.index.exists():
            self.index.delete()
        self.index.create()

    def tearDown(self):
        self.index.delete()

    def test_index_writings_entries(self):
        entry_objects = EntryFactory.create_batch(30)
        mapper = EntryMapping()
        for obj in entry_objects:
            doc_obj = mapper.to_doc(obj)
            doc_obj.save()

        self.index.refresh()
        s = Search()

        self.assertEqual(len(entry_objects), s.count())

    def test_writings_entry(self):
        entry = EntryFactory.create()
        mapper = EntryMapping()
        doc_obj = mapper.to_doc(entry)
        doc_obj.save()

        self.index.refresh()
        s = Search()
        response = s.execute()
        result = response[0]

        self.assertEqual(1, s.count())
        self.assertEqual(entry.id, result.id)
        self.assertEqual(entry.publication_date.isoformat(), result.publication_date)
        self.assertEqual(entry._meta.label, result._meta.label)
