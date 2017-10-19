import pika
from suds.client import Client
import xml.etree.ElementTree as ET
import json

# Starting connection to a RabbitMQ broker.
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Creating a queue.
channel.queue_declare(queue='g6_queue_soap_response')

# When a message is received, callback is called.
# We can override to specify its behavior.
def callback(ch, method, properties, body):
    str = bytes.decode(body)
    print(" [x] Received %r" % str)
    
    try:
        json_str = XML_translate(body)
    except (KeyError):
        send_error("Key missing, please check JSON data.", json_str)
        
    send_to_aggregator(json_str)
    
def XML_translate(body):
    xml = ET.fromstring(body)
    json_str = {}
    json_str['ssn'] = xml.find('ssn').text
    json_str['interest_rate'] = xml.find('interest').text
    json_str['bank'] = 'SOAP Bank'
    return json_str
    
def send_to_aggregator(body):

    bank_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    bank_channel = bank_connection.channel()
    
    bank_channel.queue_declare('g6_queue_aggregator')
    
    bank_channel.basic_publish(exchange='',
                               routing_key='g6_queue_aggregator',
                               body=json.dumps(body))
               
    bank_connection.close()
    
def send_error(error, body):

    # Creating a queue.
    channel.queue_declare(queue='g6_queue_dead_letter')

    json_str = {}
    json_str['error'] = error
    json_str['body'] = body
    
    # Setting up an exchange.
    channel.basic_publish(exchange='',
                          routing_key='g6_queue_dead_letter',
                          body=json.dumps(json_str))
    
channel.basic_consume(callback, queue='g6_queue_soap_response', no_ack=True)

print(" [*] Listening on queue 'g6_queue_soap_response'.")
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()