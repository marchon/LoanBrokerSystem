# 6. Modules

The Loan Broker system is made up of a large collection of small, independent components, which interface with each other in order to process and marshal information forward.

The components are created in several different languages, these languages being **Java**, **C# .NET** and **Python**. Our reasoning for this is that we felt that it would be quite relevant to create components in different languages, as the purpose of systems integration is to make systems in different languages and structures capable of communicating with each other. 

We also decided to have the majority of the components be made in Python, because those components would have a much smaller memory footprint, which will be quite relevant when running this many components at once.

We chose to make the **Credit Bureau Component** and **Aggregator** components in Java. This decision was made because we have much greater knowledge and experience with multithreading in Java, which is something we had to make use of for these components.

#### Modules

- **User Interface**

The user interface was made in Python, as we needed a simple CLI interface for sending requests to the Loan Broker system. It requests the user to input their **SSN, Loan Amount** and **Date**, which is then published to a queue consumed by the **Credit Bureau.**

- **Credit Bureau**

The credit bureau communicator was made in Java. The credit bureau communicator consumes the request sent from the user interface, and contacts the Credit Bureau we were provided. Once the credit score has been retrieved, it is added alongside the user's input, and marshalled to the **Rule Base.**

- **Rule Base**

The rule base was made in C#, and the component communicating with the rule base was made in Python. The communicator consumes the data that the Credit Bureau communicator publishes on its exchange, and then contacts the Rule Base to retrieve a list of banks to contact.

Once the list of banks has been retrieved, the rule base communicator marshals the current data along to the **Recipient List**.

- **Recipient List**

The recipient list was made in Python. The recipient list consumes the data published by the rule base communicator, and uses it to determine which banks to route the user request to.

The recipient list analyzes the list of booleans provided by the rule base to determine which banks are interested in the loan. Once it has determined which banks to route the request to, it publishes the loan request to the exchange for the translator of each bank. 

Additionally, the recipient list also contacts the **Aggregator**, informing it that a new loan request is incoming, and that it should prepare for responses for a certain SSN, and the amount of banks it should wait for before publishing the result. This was done to optimize the aggregator, something we have been given permission to from the instructor.

- **Translators/Normalizer**

The translators for every bank were made in Python. The translators come in two forms; the translators taking the request from the recipient list and forwarding it to the bank, and the translators consuming the responses from the banks, making up the **Normalizer**. 

The translators are responsible for taking the JSON string provided by the recipient list, and converting them into the data format required by their respective banks, before publishing the request to the banks.

The normalizer then consumes the responses from the banks, processes the data to remove inconsistencies between each translator, and publishes the response to the **Aggregator**.

- **Banks**

The banks were made in Python. The banks are made up of the two remote banks we were provided, the **JSON** bank and the **XML** bank, along with our own, the **SOAP** bank and the **RabbitMQ** bank.

The SOAP bank begins a SOAP web service through WSGI, and publishes a WSDL file that the translator can use to request the SOAP service. 

The RabbitMQ bank consumes CSV data with the required data.

Both banks take a 'reply_to' variable, the RabbitMQ bank taking it as a header, and the SOAP bank taking it as a variable. This variable is used by the banks to determine which queue to publish their responses to.

- **Aggregator**

The aggregator was made in Java. The aggregator consumes from two different queues; one from the recipient list, and one of the normalizer.

The *initializer* in the aggregator consumes information from the recipient list, informing it of incoming responses from the normalizer. This is done such that we can determine how many responses to wait for before publishing the result to the user, instead of having to wait for a countdown.

The *consumer* takes all responses published by the normalizer, and stores them in a key/value set, containing each SSN currently undergoing a request, the amount of banks that should respond to the request, and all current responses from the banks. Once the amount of responses matches the expected amount, the best quote is processed and published to the user interface.