import pika
import time
import random
import logging
import unittest
import json


class IntegrationTests(unittest.TestCase):

    # Starting connection to a RabbitMQ broker.
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Creating a queue.
    channel.queue_declare(queue='g6_queue_rulebase')
    
    conc_responses = {}


    def test_valid_request(self):
            
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='g6_queue_result')
        channel.basic_consume(self.callback_single, queue='g6_queue_result', no_ack=True)
        
        
        channel.basic_publish(exchange='',
                          routing_key='g6_queue_rulebase',
                          body='{"ssn": "55555555", "credit": 700, "loan": 50000, "date": 360}')
        
        channel.start_consuming()
        
    def test_concurrent_valid_requests(self):
    
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='g6_queue_result')
        channel.basic_consume(self.callback_concurrent, queue='g6_queue_result', no_ack=True)
    
        channel.basic_publish(exchange='',
                          routing_key='g6_queue_rulebase',
                          body='{"ssn": "55555555", "credit": 700, "loan": 50000, "date": 360}')
                          
                          
        channel.basic_publish(exchange='',
                          routing_key='g6_queue_rulebase',
                          body='{"ssn": "66666666", "credit": 200, "loan": 25000, "date": 150}')
                          
                          
        channel.basic_publish(exchange='',
                          routing_key='g6_queue_rulebase',
                          body='{"ssn": "77777777", "credit": 700, "loan": 800000, "date": 50}')
                          
        channel.start_consuming()
            
        
    @unittest.skip("Not a test method, used for RabbitMQ listening.")
    def callback_single(self, ch, method, properties, body):
        str = bytes.decode(body)
        json_str = json.loads(str)
        
        interest = json_str['interest_rate']
        ssn = json_str['ssn']
        bank = json_str['bank']
        
        self.assertEqual(float(interest), 2.0)
        self.assertEqual(ssn, "55555555")
        self.assertEqual(bank, 'RabbitMQ Bank')

    
    @unittest.skip("Not a test method, used for RabbitMQ listening.")
    def callback_concurrent(self, ch, method, properties, body):
        str = bytes.decode(body)
        json_str = json.loads(str)
        
        conc_responses[json_str['ssn']] = json_str
        
        if (len(conc_responses) is 3):
        
            rabbit_loan = conc_responses.get('55555555')
            xml_loan = conc_responses.get('66666666')
            json_loan = conc_responses.get('77777777')
            
            self.assertEqual(json_loan['ssn'], '55555555')
            self.assertEqual(json_loan['interest_rate'], 1.5)
            self.assertEqual(json_loan['bank'], 'JSON Bank')
            
            self.assertEqual(rabbit_loan['ssn'], '66666666')
            self.assertEqual(rabbit_loan['interest_rate'], 2.0)
            self.assertEqual(rabbit_loan['bank'], 'RabbitMQ Bank')
            
            self.assertEqual(xml_loan['ssn'], '77777777')
            self.assertEqual(xml_loan['interest_rate'], 12.768)
            self.assertEqual(xml_loan['bank'], 'XML Bank')
    

    
if __name__ == '__main__':
    unittest.main()