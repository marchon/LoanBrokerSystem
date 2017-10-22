import pika
import json
import numpy

# Starting connection to a RabbitMQ broker.
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='g6_queue_reciplist')

recipient_dict = {
                    0:'g6_exchange_xml_bank',
                    1:'g6_exchange_soap_bank',
                    2:'g6_exchange_rabbit_bank',
                    3:'g6_exchange_json_bank'
                 }

# When a message is received, callback is called.
# We can override to specify its behavior.
def callback(ch, method, properties, body):
    str = bytes.decode(body)
    print(" [x] Received %r" % str)
    json_str = json.loads(str)
    
    try:
        find_recipients(json_str, json_str['bool_list'])
    except (KeyError):
        send_error("Key missing, please check JSON data.", json_str)
    
def find_recipients(body, bool_list):

    bool_list = json.loads(bool_list)
    list = numpy.array([bool_list['Bank1'],bool_list['Bank2'],bool_list['Bank3'],bool_list['Bank4']])
    del body['bool_list']
    
    banks_to_notify = numpy.where(list == True)[0]
    notify_aggregator(body['body']['ssn'],len(banks_to_notify))

    for index, bool in enumerate(list):
        if bool:
            forward_to_bank(body,recipient_dict.get(index))
    
def notify_aggregator(ssn, bank_amount):
    
    json_str = {}
    json_str['ssn'] = ssn.replace('-','')
    json_str['bankAmount'] = bank_amount
    
    aggr_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    aggr_channel = aggr_connection.channel()
    
    aggr_channel.queue_declare('g6_queue_aggregator_initializer')
    
    aggr_channel.basic_publish(exchange='',
                          routing_key='g6_queue_aggregator_initializer',
                          body=json.dumps(json_str))
               
    print(' [*] Notified aggregator of responses for SSN: ' + ssn)
    
    aggr_connection.close()
    
def forward_to_bank(body,exchange):

    
    bank_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    bank_channel = bank_connection.channel()
    
    bank_channel.exchange_declare(exchange=exchange,
                                  exchange_type='fanout')
    
    bank_channel.basic_publish(exchange=exchange,
                          routing_key='',
                          body=json.dumps(body))
               
    print(' [*] Sent to: ' + exchange)
    
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
                          
    
channel.basic_consume(callback, queue='g6_queue_reciplist', no_ack=True)

print(' [*] Recipient List started.')
print(" [*] Listening on queue 'g6_queue_reciplist'.")
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()