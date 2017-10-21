package workers;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import java.io.IOException;
import java.util.concurrent.TimeoutException;
import java.util.logging.Level;
import java.util.logging.Logger;
import models.LoanRequest;
import org.json.JSONObject;
import services.RabbitMQService;

/**
 *
 * @author Group 6
 */
public class CreditPublisher implements Runnable {
    
    private LoanRequest loanRequest;
    
    public CreditPublisher(LoanRequest loanRequest) {
        this.loanRequest = loanRequest;
    }

    @Override
    public void run() {
        RabbitMQService service = new RabbitMQService();
        
        try (Connection conn = service.getRabbitMQConnection("localhost")) {
            Channel channel = conn.createChannel();
            service.createQueue("g6_queue_rulebase", true, false, false, null, channel);
            service.createExchange("g6_queue_rulebase", "direct", true, channel);
            service.bindExchangeQueue("g6_queue_rulebase", "g6_queue_rulebase", "", channel);
            
            String message = new JSONObject(loanRequest).toString();
            service.postToQueue(message, "g6_queue_rulebase", "", null, channel);
            channel.close();
        } catch (IOException | TimeoutException ex) {
            Logger.getLogger(CreditPublisher.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
    
}
