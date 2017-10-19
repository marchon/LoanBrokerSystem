import pika


bank_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
bank_channel = bank_connection.channel()
    
bank_channel.exchange_declare(exchange='g6_exchange_rabbit_bank',
                              exchange_type='fanout')
    
bank_channel.basic_publish(exchange='g6_exchange_rabbit_bank',
                          routing_key='',
                          body='{"body": { "ssn": "55555555", "credit": 500, "date": 360, "loan": 50000.0}}')
               
print(' [*] Sent')
    
bank_connection.close()