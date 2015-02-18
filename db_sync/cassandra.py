from cqlengine import connection
from cqlengine.management import create_keyspace

def setup_cassandra():
    connection.setup(['127.0.0.1'], "cqlengine")
    create_keyspace("cqlengine", "SimpleStrategy", 1)
