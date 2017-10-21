import pika
import sys
import json


def run():
    
    print('Welcome to the Loan Broker.')
        
    input_ssn = input('Please enter your social security number: ')
    input_loan = input('Please enter your desired loan: ')
    input_date = input('Please enter many days you would like to pay the loan back over: ')
    
    if (check_integrity(input_ssn,input_loan,input_date)):
        send_to_credit_bureau(input_ssn,input_loan,input_date)
        wait_for_result()
    
    
def check_integrity(ssn,loan,date):
    
    return True
    
def send_to_credit_bureau(ssn,loan,date):
    
    json_str = {}
    json_str['ssn'] = ssn
    json_str['amount'] = float(loan)
    json_str['days'] = int(date)
    
    credit_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    credit_channel = credit_connection.channel()
    
    credit_channel.queue_declare('g6_queue_credit', durable=True)
    
    credit_channel.basic_publish(exchange='',
                                 routing_key='g6_queue_credit',
                                 body=json.dumps(json_str))
                                 
               
    credit_connection.close()
    
    
def wait_for_result():
    
    print ('Please hold.')
    
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='g6_queue_result')
    channel.basic_consume(callback, queue='g6_queue_result', no_ack=True)
        
        
    channel.start_consuming()
    

def callback(ch, method, properties, body):

    string = bytes.decode(body)
    result_json = json.loads(string)
    
    print ('The best result is an interest rate of ' + str(result_json['interest_rate']) + ' from the ' + result_json['bank']) 
    print ('\t\t')
    
    run()
    
        
    
    
run()