
package lb_aggregator;

import com.google.gson.Gson;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.QueueingConsumer;
import java.util.ArrayList;


public class Initializer implements Runnable{

    Gson gson = new Gson();

    public Initializer() {
    }
    
    
    
    @Override
    public void run() {
        try {
            ConnectionFactory factory = new ConnectionFactory();
            factory.setHost("localhost");
            Connection connection = factory.newConnection();
            Channel channel = connection.createChannel();
            channel.queueDeclare("g6_queue_aggregator_initializer", false, false, false, null);
            QueueingConsumer consumer = new QueueingConsumer(channel);
            channel.basicConsume("g6_queue_aggregator_initializer", true, consumer);
            
            while(true){
                QueueingConsumer.Delivery delivery = consumer.nextDelivery();
                String message = new String(delivery.getBody());
                InitObject iob = gson.fromJson(message, InitObject.class);
                Dictionary.dictionary.put(iob.getSsn(), new BankResult(iob.getBankAmount(), new ArrayList<BankResponse>()));
            }
            
        } catch (Exception e){
            
        }
    }

    private static class InitObject {

        String ssn;
        int bankAmount;
        
        public InitObject(String ssn, int bankAmount) {
            this.ssn = ssn;
            this.bankAmount = bankAmount;
        }

        public String getSsn() {
            return ssn;
        }

        public void setSsn(String ssn) {
            this.ssn = ssn;
        }

        public int getBankAmount() {
            return bankAmount;
        }

        public void setBankAmount(int bankAmount) {
            this.bankAmount = bankAmount;
        }
        
        
    }
    
}
