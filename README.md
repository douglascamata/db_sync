# Requirements

- Python 3.4.x
- ElasticSearch installed and running on default port
- Cassandra installed and running on default port

# Run instructions

Install the package with `python setup.py install` and to run the daemon execute `python sync_daemon.py start`.

By default, the daemon will synchronize the databases each 5 seconds. You can change this by passing the command-line argument `--time` with the number of seconds you want to poll the databases, for example, the following command will synchronize the databses each 10 seconds:

`python sync_daemon.py start --time 10`

To stop, you may use `python sync_daemon.py stop`.

