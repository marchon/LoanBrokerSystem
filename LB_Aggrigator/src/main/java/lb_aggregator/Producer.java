package lb_aggregator;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.MessageProperties;

public class Producer {

    Channel channel;
    String answer;

    Producer() {
        }

    public void publishResult(String ssn, double interest_rate, String Bank) {
        try {
            ConnectionFactory factory = new ConnectionFactory();
            factory.setHost("localhost");
            Connection connection = factory.newConnection();
            Channel channel = connection.createChannel();
            channel.queueDeclare("g6_queue_result", false, false, false, null);
            String message = "{ \"ssn\": \"" + ssn + "\", \"interest_rate\" : " + interest_rate + " , \"bank\" : " + Bank + "\" }";
            channel.basicPublish("", "g6_queue_result", null, message.getBytes());
            connection.close();
        } catch (Exception e) {
            System.out.println("ass");
        }
    }

}
