import pika
from suds.client import Client
import xml.etree.ElementTree as ET
import json

# Starting connection to a RabbitMQ broker.
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='g6_bank_rabbit',
                                  exchange_type='fanout')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='g6_bank_rabbit',
                   queue=queue_name)

# When a message is received, callback is called.
# We can override to specify its behavior.
def callback(ch, method, properties, body):
    # SSN,Loan,Date,Credit
    str = bytes.decode(body)
    loan_tuple = str.split(",")
    print(" [x] Received %r" % str)
    if validate_loan(loan_tuple):
        send_response(loan_tuple[0])
    else:
        send_error(str)
    
def validate_loan(tuple):
    
    print (tuple)

    # Checking if any of the parameters are missing.
    if (len(tuple) is not 4):
        return False
        
    if None in [tuple[0],tuple[1],tuple[2],tuple[3]]:
        return False
    
    if int(tuple[3]) >= 400:
        return True
    else:
        return False
    
def send_response(ssn):

    json_str ='{"ssn" : ' + ssn + ', "interest" : 2.0 }'
    
    bank_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    bank_channel = bank_connection.channel()
    
    bank_channel.exchange_declare(exchange='g6_exchange_rabbit_response',
                                  exchange_type='fanout')
    
    bank_channel.basic_publish(exchange='g6_exchange_rabbit_response',
                               routing_key='',
                               body=json_str)
               
    bank_connection.close()


                          
def send_error(body):
    
    # Creating a queue.
    channel.queue_declare(queue='g6_queue_dead_letter')

    json_str = {}
    json_str['error'] = "Error occurred. This loan is either poorly formatted, or does not meet this bank's criteria."
    json_str['body'] = body
    
    # Setting up an exchange.
    channel.basic_publish(exchange='',
                          routing_key='g6_queue_dead_letter',
                          body=json.dumps(json_str))
                          
                          
channel.basic_consume(callback, queue=queue_name, no_ack=True)

print(" [*] Listening on exchange 'g6_bank_rabbit'.")
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()