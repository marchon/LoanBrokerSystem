from suds.client import Client
import logging
import unittest
import xml.etree.ElementTree as ET
import pika
import json

class TestSOAPBank(unittest.TestCase):
    
    
    def test_valid_request_good_credit(self):
        
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='g6_bank_rabbit')
        channel.queue_declare(queue='g6_queue_rabbit_response')
        
        channel.basic_consume(self.callback, queue='g6_queue_rabbit_response', no_ack=True)
        
        channel.basic_publish(exchange='',
                              routing_key='g6_bank_rabbit',
                              body="555555-5555,50000.0,360,500")
        
        channel.start_consuming()
        
    def test_invalid_loan_too_low_credit(self):
        
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='g6_bank_rabbit')
        channel.queue_declare(queue='g6_queue_dead_letter')
        
        channel.basic_consume(self.callback_low_credit, queue='g6_queue_dead_letter', no_ack=True)
        
        channel.basic_publish(exchange='',
                              routing_key='g6_bank_rabbit',
                              body="555555-5555,50000.0,360,200")
        
        channel.start_consuming()
        
        
    
    def test_invalid_loan_bad_input(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='g6_bank_rabbit')
        channel.queue_declare(queue='g6_queue_dead_letter')
        
        channel.basic_consume(self.callback_bad_values, queue='g6_queue_dead_letter', no_ack=True)
        
        channel.basic_publish(exchange='',
                              routing_key='g6_bank_rabbit',
                              body="50000.0,360,200")
        
        channel.start_consuming()
        
        
    @unittest.skip("Not a test method, used for RabbitMQ listening.")
    def callback(self, ch, method, properties, body):
        
        str = bytes.decode(body)
        print (str)
        
        self.assertEqual(str, '{"ssn" : "555555-5555", "interest" : 2.0}')
        
        
    @unittest.skip("Not a test method, used for RabbitMQ listening.")
    def callback_low_credit(self, ch, method, properties, body):
        str = bytes.decode(body)
        print (str)
        
        json_str = json.loads(str)
        
        self.assertEqual(json_str['error'], 'Error occurred. This loan is either poorly formatted, or does not meet this bank\'s criteria.')
        self.assertEqual(json_str['body'], '555555-5555,50000.0,360,200')
        

    @unittest.skip("Not a test method, used for RabbitMQ listening.")
    def callback_bad_values(self, ch, method, properties, body):
        str = bytes.decode(body)
        print (str)
        
        json_str = json.loads(str)
        
        self.assertEqual(json_str['error'], 'Error occurred. This loan is either poorly formatted, or does not meet this bank\'s criteria.')
        self.assertEqual(json_str['body'], '50000.0,360,200')
        
    

if __name__ == '__main__':
    unittest.main()