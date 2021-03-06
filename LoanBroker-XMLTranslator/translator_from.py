import pika
from suds.client import Client
import xml.etree.ElementTree as ET
import json

# Starting connection to a RabbitMQ broker.
connection = pika.BlockingConnection(pika.URLParameters('amqp://student:cph@datdb.cphbusiness.dk:5672/%2F'))
channel = connection.channel()

channel.queue_declare(queue='g6_queue_xml_response')

# When a message is received, callback is called.
# We can override to specify its behavior.
def callback(ch, method, properties, body):
    str = bytes.decode(body)
    print(" [x] Received %r" % str)
    try:
        json_str = XML_translate(body)
        send_to_aggregator(json_str)
    except (KeyError):
        # Publishing the rejected data to a dead letter queue.
        send_error("Key missing, please check JSON data.", json_str)
    
def XML_translate(body):
    xml = ET.fromstring(body)
    json_str = {}
    json_str['ssn'] = xml.find('ssn').text
    json_str['interest_rate'] = xml.find('interestRate').text
    json_str['bank'] = 'XML Bank'
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

    channel.queue_declare(queue='g6_queue_dead_letter')

    json_str = {}
    json_str['error'] = error
    json_str['body'] = body
    
    channel.basic_publish(exchange='',
                          routing_key='g6_queue_dead_letter',
                          body=json.dumps(json_str))
    
channel.basic_consume(callback, queue='g6_queue_xml_response', no_ack=True)

print(" [*] Listening on queue 'g6_queue_xml_response'.")
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()