from suds.client import Client
import logging

credit_client = Client('http://138.68.85.24:8080/CreditScoreService/CreditScoreService?wsdl')

print (credit_client.service.creditScore("567678-6666"))