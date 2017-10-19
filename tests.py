import pika
import time
import random


def test_valid_request_good_credit():
        
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='g6_queue_result')
    channel.basic_consume(callback, queue='g6_queue_result', no_ack=True)
        
    channel.start_consuming()
    
def callback(ch, method, properties, body):
    str = bytes.decode(body)
    print(str)

# Starting connection to a RabbitMQ broker.
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Creating a queue.
channel.queue_declare(queue='g6_queue_aggregator_initializer')


# Setting up an exchange.
#channel.basic_publish(exchange='',
#                      routing_key='g6_queue_rulebase',
#                      body='{"ssn": "5555555555", "credit": 500, "loan": 50000, "date": 360}')

channel.basic_publish(exchange='',
                      routing_key='g6_queue_aggregator_initializer',
                      body='{"ssn": "5555555555", "bankAmount": 3}')
                      
channel.basic_publish(exchange='',
                      routing_key='g6_queue_aggregator_initializer',
                      body='{"ssn": "5555555556", "bankAmount": 3}')
print(" [x] Sent ")

time.sleep(5)

channel.basic_publish(exchange='',
                    routing_key='g6_queue_aggregator',
                    body='{"ssn": "5555555555", "interest_rate": 3.5, "bank": "Cool Bank"}')
                    
                    
channel.basic_publish(exchange='',
                    routing_key='g6_queue_aggregator',
                    body='{"ssn": "5555555555", "interest_rate": 4.5, "bank": "Mediocre Bank"}')
                    
channel.basic_publish(exchange='',
                    routing_key='g6_queue_aggregator',
                    body='{"ssn": "5555555556", "interest_rate": 1.5, "bank": "Fuckin Nice Bank"}')
                    
channel.basic_publish(exchange='',
                    routing_key='g6_queue_aggregator',
                    body='{"ssn": "5555555556", "interest_rate": 2.5, "bank": "Jyske Bank"}')
                    
                    
channel.basic_publish(exchange='',
                    routing_key='g6_queue_aggregator',
                    body='{"ssn": "5555555555", "interest_rate": 8.5, "bank": "Shit Bank"}')
                        
                      
                      
print(" [x] Sent ")

test_valid_request_good_credit()

connection.close()