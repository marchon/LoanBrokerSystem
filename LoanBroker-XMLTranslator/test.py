import pika
import json
from suds.client import Client
import lxml.etree
import lxml.builder
import arrow


bank_connection = pika.BlockingConnection(pika.URLParameters('amqp://student:cph@datdb.cphbusiness.dk:5672/%2F'))
bank_channel = connection.channel()
    
body = "<LoanRequest><ssn>12345678</ssn><creditScore>685</creditScore><loanAmount>1000.0</loanAmount><loanDuration>1973-01-01 01:00:00.0 CET</loanDuration></LoanRequest>"
    
bank_channel.basic_publish(exchange='cphbusiness.bankXML',
                      routing_key='',
                      body=body,
                      properties=pika.BasicProperties(reply_to='xml_response_queue_6'))
               
print(" [x] Sent ")
    
bank_connection.close()
    
