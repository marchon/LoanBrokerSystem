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
            chann.queueDeclare("g6_queue_result", false, false, false, null);
            String message = "{ \"ssn\": \"" + ssn + "\", \"interest_rate\" : " + interest_rate + " , \"bank\" : \"" + Bank + "\" }";
            chann.basicPublish("", "g6_queue_result", null, message.getBytes());
            System.out.println(" [*] Sent message to user response channel");
            connection.close();
        } catch (IOException e) {
            System.out.println("ass");
        }
    }

}
