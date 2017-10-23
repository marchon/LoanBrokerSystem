# Application connects service definitions, interfaces and protocols.
from spyne.application import Application
# Exposes methods for remote procedure calls, and declares data types, allowing for WSDL generation.
from spyne.decorator import srpc, rpc
# Service definition base class.
from spyne.service import ServiceBase
# The type we're accepting for the service.
from spyne.model.complex import Unicode
# Web Server Gateway Interface, allows us to use HTTP for calls.
from spyne.server.wsgi import WsgiApplication
# Python's stock WSGI server.
from wsgiref.simple_server import make_server
# Protocol for our SOAP service
from spyne.protocol.soap import Soap11
# Python's default logger
import logging
# RabbitMQ module
import pika
import lxml.etree
import lxml.builder

class SOAPBankService(ServiceBase):
    
    
    @srpc(Unicode, Unicode, Unicode, Unicode, Unicode, _returns=Unicode)
    def give_loan(ssn, credit, loan_amount, date, queue):
        
        if AppMethods.data_is_missing(ssn, credit, loan_amount, date, queue):
            # Creating XML response with an error message.
            xml = lxml.builder.ElementMaker()
            doc = xml.doc
            response = xml.response
            return lxml.etree.tostring(doc(response("Invalid request. Please include all parameters.")), pretty_print=True)
        
        if AppMethods.credit_is_sufficient_for_loan(credit, loan_amount):
            # Publish SSN and interest rate as XML response.
            xml = AppMethods.xml_response(ssn)
            RabbitMethods.publish_loan_response(xml, queue)
            #return AppMethods.xml_response(ssn)
        else:
            # Creating XML response with error message.
            xml = lxml.builder.ElementMaker()
            doc = xml.doc
            response = xml.response
            return lxml.etree.tostring(doc(response("Loan denied.")), pretty_print=True)
    
        
        
class AppMethods(Application):

    def data_is_missing(ssn, credit, loan_amount, date, queue):
        # Checking if any of the parameters are missing.
        if None in [ssn, credit, loan_amount, date, queue]:
            return True
        else:
            return False
    
    def credit_is_sufficient_for_loan(credit, loan):
        # If credit score is 200 or above, allow loans above 20,000.
        if int(credit) >= 200:
            return True
        else:
            # If not above 200, only allow loans at 20,000 or below.
            return float(loan) <= 20000.0
            
    def xml_response(ssn):
        xml = lxml.builder.ElementMaker()
        doc = xml.doc
        interest_field = xml.interest
        ssn_field = xml.ssn
        
        xml_doc = doc(
                    interest_field("7.5"),
                    ssn_field(ssn),
                    )
        
        return lxml.etree.tostring(xml_doc, pretty_print=True)
        
        
        
class RabbitMethods(Application):
    
    def publish_loan_response(xml_response, queue):
    
        # Starting connection to a RabbitMQ broker.
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        # Creating a queue if it does not exist. Method is idempotent; does nothing if the queue exists.
        channel.queue_declare(queue=queue)
        
        # Setting up an exchange.
        channel.basic_publish(exchange='',
                      routing_key=queue,
                      body=xml_response)
                      
        print(" [x] Sent ")
        
        connection.close()
    
    
    
    
    
app = Application([SOAPBankService], 'spyne.examples.hello.http',
                    in_protocol=Soap11(validator='lxml'),
                    out_protocol=Soap11(),
                    )
    
wsgi_app = WsgiApplication(app)
        
        
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)
        
    server = make_server('127.0.0.1', 7789, wsgi_app)
        
    print ("listening to http://127.0.0.1:7789")
    print ("wsdl is at: http://localhost:7789/?wsdl")
        
    server.serve_forever()