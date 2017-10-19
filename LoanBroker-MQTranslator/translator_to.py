import pika
import json
from suds.client import Client
import xml.etree.ElementTree as ET

# Starting connection to a RabbitMQ broker.
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='g6_exchange_rabbit_bank',
                                  exchange_type='fanout')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='g6_exchange_rabbit_bank',
                   queue=queue_name)

# When a message is received, callback is called.
# We can override to specify its behavior.
def callback(ch, method, properties, body):
    string = bytes.decode(body)
    print(" [x] Received %r" % string)
    try:
        json_str = json.loads(string)
        json_str = json_str['body']
        csv_str = json_str['ssn'] + "," + str(json_str['loan']) + "," + str(json_str['date']) + "," + str(json_str['credit'])
        send_to_bank(csv_str)
    except (KeyError):
        send_error("Key missing, please check JSON data.", json_str)
    
def send_to_bank(body):

    bank_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    bank_channel = bank_connection.channel()
    
    bank_channel.exchange_declare(exchange='g6_bank_rabbit',
                                  exchange_type='fanout')
    
    bank_channel.basic_publish(exchange='g6_bank_rabbit',
                               routing_key='',
                               body=body)
               
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
                          
    
channel.basic_consume(callback, queue=queue_name, no_ack=True)

print(" [*] Listening on exchange 'g6_exchange_rabbit_bank'.")
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()