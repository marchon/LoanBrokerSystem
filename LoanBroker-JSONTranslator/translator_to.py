import pika
from suds.client import Client
import json

# Starting connection to a RabbitMQ broker.
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='g6_exchange_json_bank',
                                  exchange_type='fanout')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='g6_exchange_json_bank',
                   queue=queue_name)


# When a message is received, callback is called.
# We can override to specify its behavior.
def callback(ch, method, properties, body):
    str = bytes.decode(body)
    print(" [x] Received %r" % str)
    try:
        json_str = json.loads(str)
        form_json = construct_json(json_str['body'])
        send_to_bank(form_json)
    except (KeyError):
        send_error("Key missing, please check JSON data.", json_str)
    
def construct_json(body):
    
    formatted_json = {}
    formatted_json["ssn"] = int(body['ssn'])
    formatted_json["creditScore"] = body['credit']
    formatted_json["loanAmount"] = body['loan']
    formatted_json["loanDuration"] = body['date']
    return formatted_json
    
    
def send_to_bank(body):

    print (body)

    bank_connection = pika.BlockingConnection(pika.URLParameters('amqp://student:cph@datdb.cphbusiness.dk:5672/%2F'))
    bank_channel = bank_connection.channel()
    
    bank_channel.basic_publish(exchange='cphbusiness.bankJSON',
                      routing_key='',
                      body=json.dumps(body),
                      properties=pika.BasicProperties(reply_to='g6_queue_json_response'))
               
    print(" [x] Sent ")
    
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

print(" [*] Listening on queue 'g6_exchange_json_bank'.")
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

