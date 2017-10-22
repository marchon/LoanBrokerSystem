package lb_aggregator.channels;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import java.io.IOException;

public class Producer {

    Channel channel;
    String answer;

    public Producer() {
        
        }

    public void publishResult(String ssn, double interest_rate, String Bank) {
        try {
            ConnectionFactory factory = new ConnectionFactory();
            factory.setHost("localhost");
            
            Connection connection = factory.newConnection();
            Channel chann = connection.createChannel();
            
            // We set up a specific channel for the SSN, that the user interface consumes from.
            // Not a perfect solution, but we're doing what we can with what we're given.
            // Some kind of UID from the user interface would have been preferable, but not doable due to the remote banks.
            String queue = "g6_queue_result_" + ssn;
            
            chann.queueDeclare(queue, false, false, false, null);
            String message = "{ \"ssn\": \"" + ssn + "\", \"interest_rate\" : " + interest_rate + " , \"bank\" : \"" + Bank + "\" }";
            
            chann.basicPublish("", queue, null, message.getBytes());
            System.out.println(" [*] Sent message to user response channel");
            connection.close();
        } catch (IOException e) {
            
        }
    }

}
