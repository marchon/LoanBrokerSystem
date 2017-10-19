# Loan Broker - SOAP Bank

This is an educational repository for the Loan Broker semester project, on the Software Development bachelor program at Copenhagen Business Academy.



### Dependencies

- [Python 3.6](https://www.python.org/)
- [Spyne](spyne.io)
- [suds-jurko](https://bitbucket.org/jurko/suds)

Running the script file `install_dependencies.sh` will install these dependencies. Alternatively, these dependencies can be installed manually through `PiPy`:

```bash
$ pip install spyne
$ pip install suds-jurko
```



### How to run

Running the server requires running the `server.py` script. 

```bash
$ py -u server.py
```

This will start the server, and open the SOAP server and the WSDL file on the following addresses:

```
Server: http://127.0.0.1:7789

WSDL: http://127.0.0.1:7789/?wsdl
```

There is a script for testing the server, named `tests.py`, which uses `suds-jurko` to send a request to the SOAP service:

```bash
$ py -u tests.py
```

