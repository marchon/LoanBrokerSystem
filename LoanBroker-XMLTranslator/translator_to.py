import pika
import json
import lxml.etree
import lxml.builder
import arrow

# Starting connection to a RabbitMQ broker.
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='g6_exchange_xml_bank',
                                  exchange_type='fanout')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='g6_exchange_xml_bank',
                   queue=queue_name)

# When a message is received, callback is called.
# We can override to specify its behavior.
def callback(ch, method, properties, body):
    str = bytes.decode(body)
    print(" [x] Received %r" % str)
    try:
        json_str = json.loads(str)
        xml_str = generate_xml(json_str['body'])
        send_to_bank(bytes.decode(xml_str))
    except (KeyError):
        # Publishing the rejected data to a dead letter queue.
        send_error("Key missing, please check JSON data.", json_str)
    
def generate_xml(json_str):
    xml = lxml.builder.ElementMaker()
    doc = xml.LoanRequest
    ssn_field = xml.ssn
    credit_field = xml.creditScore
    loan_field = xml.loanAmount
    date_field = xml.loanDuration
    
    datetime_str = generate_datetime_string(json_str['date'])
    datetime_str = datetime_str.format().split("+",1)[0] + ".0 CET"
        
    xml_doc = doc(
                ssn_field(str(json_str['ssn'].replace('-',''))),
                credit_field(str(json_str['credit'])),
                loan_field(str(json_str['loan'])),
                date_field(datetime_str.format())
                )
        
    return lxml.etree.tostring(xml_doc)
    
def generate_datetime_string(date):
    
    # Generating the base date, then incrementing by the number of days.
    base_date = arrow.get('1970-01-01 01:00:00')
    return base_date.replace(days=+date)
    
def send_to_bank(body):
    bank_connection = pika.BlockingConnection(pika.URLParameters('amqp://student:cph@datdb.cphbusiness.dk:5672/%2F'))
    bank_channel = bank_connection.channel()
    
    bank_channel.basic_publish(exchange='cphbusiness.bankXML',
                      routing_key='',
                      body=body,
                      properties=pika.BasicProperties(reply_to='g6_queue_xml_response'))
               
    print(" [x] Sent ")
    
    bank_connection.close()
 

def send_error(error, body):

    channel.queue_declare(queue='g6_queue_dead_letter')

    json_str = {}
    json_str['error'] = error
    json_str['body'] = body
    
    channel.basic_publish(exchange='',
                          routing_key='g6_queue_dead_letter',
                          body=json.dumps(json_str))
    
channel.basic_consume(callback, queue=queue_name, no_ack=True)

print(" [*] Listening on queue 'g6_exchange_xml_bank'.")
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

