import pika
import json
import requests

# Starting connection to a RabbitMQ broker.
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='g6_queue_rulebase')


# When a message is received, callback is called.
# We can override to specify its behavior.
def callback(ch, method, properties, body):
    str = bytes.decode(body)
    print(" [x] Received %r" % str)
    try:
        json_str = json.loads(str)
        get_bank_list(json_str)
    except (KeyError):
        send_error("Key missing, please check JSON data.", json_str)
    
def get_bank_list(json_str):

    r = requests.get('http://localhost:51785/api/bankrules/' + str(json_str['credit']) + '/' + str(json_str['loan']))
    
    full_json = {}
    full_json['body'] = json_str
    full_json['bool_list'] = r.text
    
    forward_to_recipient_list(full_json)
    
    
def forward_to_recipient_list(body):
    
    rec_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    rec_channel = rec_connection.channel()
    
    rec_channel.queue_declare('g6_queue_reciplist')
    
    rec_channel.basic_publish(exchange='',
                              routing_key='g6_queue_reciplist',
                              body=json.dumps(body))
               
    rec_connection.close()
                          
                          
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
    
channel.basic_consume(callback, queue='g6_queue_rulebase', no_ack=True)

print(' [*] Rule Base Component started.')
print(" [*] Listening on queue 'g6_queue_rulebase'.")
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()