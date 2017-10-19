# Loan Broker - SOAP Translator

This is an educational repository for the Loan Broker semester project, on the Software Development bachelor program at Copenhagen Business Academy.



### Dependencies

- [Python 3.6](https://www.python.org/)
- [pika](https://pika.readthedocs.io/en/0.10.0/)
- [suds-jurko](https://bitbucket.org/jurko/suds)

Running the script file `install_dependencies.sh` will install these dependencies. Alternatively, these dependencies can be installed manually through `PiPy`:

```bash
$ pip install pika
$ pip install suds-jurko
```



### How to run

Running the translator requires running the `translator.py` script. 

```bash
$ py -u translator.py
```

This will start the translator, and cause it to listen on the `soap_bank` channel for now.


There is a script for testing the server, named `client.py`, which uses `suds-jurko` to send a request to the SOAP service:

```bash
$ py -u test.py
```
