import pika

# Starting connection to a RabbitMQ broker.
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Creating a queue.
channel.queue_declare(queue='g6_queue_rulebase')


# Setting up an exchange.
channel.basic_publish(exchange='',
                      routing_key='g6_queue_rulebase',
                      body='{"ssn": "5555555555", "credit": 500, "loan": 50000, "date": 360}')
print(" [x] Sent ")

connection.close()