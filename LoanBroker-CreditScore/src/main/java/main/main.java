package main;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import java.io.IOException;
import java.util.concurrent.TimeoutException;
import java.util.logging.Level;
import java.util.logging.Logger;
import workers.CreditConsumer;

public class main {

    private static int numberOfWorkers;

    public static void main(String[] args) throws IOException {

        try {
            System.out.println("CreditScore application running...");
            
            ConnectionFactory factory = new ConnectionFactory();
            factory.setHost("localhost");
            Connection connection = factory.newConnection();
            Channel channel = connection.createChannel();
            
            channel.queueDeclare("g6_queue_credit", true, false, false, null);
            channel.basicConsume("g6_queue_credit", true, new CreditConsumer(channel));
            
            System.out.println(" [*] Waiting for messages. To exit press CTRL+C");
        } catch (TimeoutException ex) {
            Logger.getLogger(main.class.getName()).log(Level.SEVERE, null, ex);
        }
        
        
    }
}
