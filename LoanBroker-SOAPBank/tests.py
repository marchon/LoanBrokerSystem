from suds.client import Client
import logging
import unittest
import xml.etree.ElementTree as ET
import pika

class TestSOAPBank(unittest.TestCase):
    
    soap_client = Client('http://localhost:7789/?wsdl')
    
    def test_valid_request_good_credit(self):
        
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='server_test_queue')
        channel.basic_consume(self.callback, queue='server_test_queue', no_ack=True)
        
        self.soap_client.service.give_loan("55555-5555",500,80000.00,"260",'server_test_queue')
        
        channel.start_consuming()
        

    def test_invalid_loan_too_low_credit(self):
        
        response = self.soap_client.service.give_loan("55555-5555",150,80000.00,"260",'server_test_queue')
        xml = ET.fromstring(response)
        
        
        response = xml.find('response').text
        
        self.assertEqual(response, "Loan denied.")
        
    
    def test_invalid_loan_bad_input(self):
        response = self.soap_client.service.give_loan("55555-5555","260")
        xml = ET.fromstring(response)
        
        
        response = xml.find('response').text
        
        self.assertEqual(response, "Invalid request. Please include all parameters.")
        
    @unittest.skip("Not a test method, used for RabbitMQ listening.")
    def callback(self, ch, method, properties, body):
        str = bytes.decode(body)
        xml = ET.fromstring(str)
        
        interest = xml.find('interest').text
        ssn = xml.find('ssn').text
        
        self.assertEqual(float(interest), 7.5)
        self.assertEqual(ssn, "55555-5555")
    

if __name__ == '__main__':
    unittest.main()