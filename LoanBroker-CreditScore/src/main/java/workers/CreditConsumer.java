package workers;

import com.rabbitmq.client.AMQP;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.DefaultConsumer;
import com.rabbitmq.client.Envelope;
import java.io.IOException;
import models.LoanRequest;
import org.json.JSONObject;
import services.CreditScoreService;

/**
 *
 * @author Group 6
 */
public class CreditConsumer extends DefaultConsumer {

    public CreditConsumer(Channel channel) {
        super(channel);
    }

    @Override
    public void handleDelivery(String consumerTag, Envelope envelope, AMQP.BasicProperties properties, byte[] body) throws IOException {
        JSONObject json = convertToJSON(body);
        String ssn = (String) json.get("ssn");

        int creditScore = getCreditScore(ssn);
        LoanRequest lr = createLoanRequest(json, creditScore);
        System.out.println("Message broadcasted");
        broadcast(lr);
    }

    /**
     * Converts a byte[] into a JSONobject.
     *
     * @param body
     * @return JSONObject
     */
    private JSONObject convertToJSON(byte[] body) {
        String jsonString = new String(body);
        return new JSONObject(jsonString);
    }

    /**
     * Takes a ssn and retrieves a credit score from the SOAP service.
     *
     * @param ssn
     * @return int
     */
    private int getCreditScore(String ssn) {
        CreditScoreService cs = new CreditScoreService();
        return cs.getCreditScore(ssn);
    }

    /**
     * Generates a LoanRequest object from the json retrieved fromm the client
     * and with the credit score retrieved from the SOAP service.
     *
     * @param json
     * @param creditScore
     * @return LoanRequest
     */
    private LoanRequest createLoanRequest(JSONObject json, int creditScore) {
        json.append("creditScore", creditScore);
        LoanRequest lr = new LoanRequest(
                (String) json.get("ssn"),
                creditScore,
                (Double) json.get("amount"),
                (int) json.get("days")
        );
        return lr;
    }

    /**
     * Broadcasts a LoanRequest to the system via the CreditPublisher class.
     *
     * @param lr
     */
    private void broadcast(LoanRequest lr) {
        CreditPublisher p = new CreditPublisher(lr);
        p.run();
    }
}
