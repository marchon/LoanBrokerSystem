
package lb_aggregator;

import com.google.gson.Gson;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.QueueingConsumer;

public class Consumer {

    Producer p = new Producer();
    Gson gson = new Gson();
    public void Consume(){
        try {
            ConnectionFactory factory = new ConnectionFactory();
            factory.setHost("localhost");
            Connection connection = factory.newConnection();
            Channel channel = connection.createChannel();
            channel.queueDeclare("g6_queue_aggregator", false, false, false, null);
            QueueingConsumer consumer = new QueueingConsumer(channel);
            channel.basicConsume("g6_queue_aggregator", true, consumer);
            
            while(true){
                QueueingConsumer.Delivery delivery = consumer.nextDelivery();
                String message = new String(delivery.getBody());
                BankResponse bankResponse = gson.fromJson(message, BankResponse.class);
               if(Dictionary.checkResultAmount(bankResponse.getSsn())){
                  BankResponse me = Dictionary.checkBestResult(bankResponse.getSsn());
                  p.publishResult(me.getSsn(),me.getInterest_rate(),me.getBank());
               }
            }
            
        } catch (Exception e){
            
        }
    }
}
