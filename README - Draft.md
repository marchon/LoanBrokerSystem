# Loan Broker System
### Dependencies

The full Loan Broker system requires several dependencies and languages to be installed. The languages required are:

- **Java 8**
- **C# .NET Core**
- **Python 3.6**
- **Erlang**

Dependencies for the Java and .NET projects are handled by their respective package managers. Dependencies for the Python scripts can all be installed by running the `install_dependencies.sh` script.

Additionally, this system requires that you have **RabbitMQ** installed locally, and that the system in use has online access, as several components are located on a remote server.

### Running

Every standalone component can be run by navigating to their respective folder and executing the shell scripts therein. Alternatively, every component can be run at once by executing the `run_all.sh` script in the root folder.

To ensure that every component is running correctly, you can execute the `run_integration_tests.sh` script in the root folder, which will perform a full integration test throughout every component in the system. There are also individual tests for the SOAP Bank and RabbitMQ Bank components, located in their respective folders.