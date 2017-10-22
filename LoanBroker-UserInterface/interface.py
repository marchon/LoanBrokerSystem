import pika
import sys
import json

credit_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
credit_channel = credit_connection.channel()

def run():
    
    print('Welcome to the Loan Broker.')
        
    while (True):
    
        input_ssn = input('Please enter your social security number: ')
        input_loan = input('Please enter your desired loan: ')
        input_date = input('Please enter many days you would like to pay the loan back over: ')
    
        if (check_integrity(input_ssn,input_loan,input_date)):
            send_to_credit_bureau(input_ssn,input_loan,input_date)
            wait_for_result(input_ssn)
    
    
    
def check_integrity(ssn,loan,date):
    
    ssn = ssn.replace('-','')
    
    try:
        int(ssn)
        float(loan)
        int(date)
        
        if (int(ssn) <= 2147483647 and int(ssn) > 0 and int(date) > 0 and float(loan) > 0):
            return True
    except:
        print ('')
        print ('Your input seems to contain at least one error.')
        print ('Your SSN should follow the structure of "xxxxxx-xxxx".')
        print ('Your loan should only contain numbers.')
        print ('Your loan duration should only contain the number of days desired.')
        print ('')
        return False
    
def send_to_credit_bureau(ssn,loan,date):
    
    json_str = {}
    json_str['ssn'] = ssn
    json_str['amount'] = float(loan)
    json_str['days'] = int(date)
    
    
    credit_channel.queue_declare('g6_queue_credit', durable=True)
    
    
    credit_channel.basic_publish(exchange='',
                                 routing_key='g6_queue_credit',
                                 body=json.dumps(json_str))
                                 
    
def wait_for_result(ssn):
    
    print ('Please hold.')
    
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    queue = 'g6_queue_result_' + ssn.replace('-','')
    
    channel.queue_declare(queue=queue)
    channel.basic_consume(callback, queue=queue, no_ack=True)
        
        
    channel.start_consuming()
    

def callback(ch, method, properties, body):

    string = bytes.decode(body)
    result_json = json.loads(string)
    
    print ('The best result is an interest rate of ' + str(result_json['interest_rate']) + ' from the ' + result_json['bank']) 
    print ('\t\t')
    
    ch.stop_consuming()
    ch.close()
    
    
    run()
    
        
    
    
run()