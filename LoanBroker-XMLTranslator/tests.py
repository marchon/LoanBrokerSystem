import pika

# Starting connection to a RabbitMQ broker.
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Creating a queue.
channel.queue_declare(queue='xml_bank')


# Setting up an exchange.
channel.basic_publish(exchange='',
                      routing_key='xml_bank',
                      body='{"ssn":1605789787,"credit":598,"loan":10.0,"date":360}')
print(" [x] Sent ")

connection.close()