# Requirements

- Python 3.4.x

# Run instructions

Install the package with `python setup.py install` and to run the daemon execute `python daemon.py`.

By default, the daemon will synchronize the databases each 5 seconds. You can change this by passing the command-line argument `--time` with the number of seconds you want to poll the databases, for example, the following command will synchronize the databses each 10 seconds:

`python daemon.py --time 10`

