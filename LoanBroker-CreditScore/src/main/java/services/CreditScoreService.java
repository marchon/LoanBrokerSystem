package services;

/***
 * Services to contact WSDL Credit Score SOAP Service
 * 
 * @author Group 6
 */
public class CreditScoreService implements ICreditScoreService{
    
    @Override
    public int getCreditScore(String ssn) {
        int result = 0;
        try { // Call Web Service Operation
            org.bank.credit.web.service.CreditScoreService_Service service = new org.bank.credit.web.service.CreditScoreService_Service();
            org.bank.credit.web.service.CreditScoreService port = service.getCreditScoreServicePort();
            // TODO initialize WS operation arguments here
            // TODO process result here
            result = port.creditScore(ssn);
        } catch (Exception ex) {
            throw ex;
        }
        return result;
    }
}
