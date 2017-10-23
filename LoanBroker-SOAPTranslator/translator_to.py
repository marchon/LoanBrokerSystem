import pika
from suds.client import Client
import json

# Starting connection to a RabbitMQ broker.
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='g6_exchange_soap_bank',
                                  exchange_type='fanout')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='g6_exchange_soap_bank',
                   queue=queue_name)

# When a message is received, callback is called.
# We can override to specify its behavior.
def callback(ch, method, properties, body):
    str = bytes.decode(body)
    print(" [x] Received %r" % str)
    json_str = json.loads(str)
    try:
        SOAP_translate(json_str['body'])
    except (KeyError):
        # Publishing the rejected data to a dead letter queue.
        send_error("Key missing, please check JSON data.", json_str)
    
    
    
def SOAP_translate(body):
    try:
        # Instantiating a SOAP client through suds.
        soap_client = Client('http://localhost:7789/?wsdl')
        
        soap_client.service.give_loan(body['ssn'],body['credit'],body['loan'],body['date'],'g6_queue_soap_response')
    except (suds.WebFault|suds.transport.TransportError|urllib.error.HTTPError):
        # Publishing the rejected data to a dead letter queue.
        send_error("SOAP web service encountered an unknown error.", body)
    
def send_error(error, body):

    channel.queue_declare(queue='g6_queue_dead_letter')

    json_str = {}
    json_str['error'] = error
    json_str['body'] = body
    
    channel.basic_publish(exchange='',
                          routing_key='g6_queue_dead_letter',
                          body=json.dumps(json_str))
    
channel.basic_consume(callback, queue=queue_name, no_ack=True)

print(" [*] Listening on queue 'g6_exchange_soap_bank'.")
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()