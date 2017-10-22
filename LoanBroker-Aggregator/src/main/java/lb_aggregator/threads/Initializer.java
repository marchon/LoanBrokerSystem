package lb_aggregator.threads;

import lb_aggregator.models.BankResponse;
import lb_aggregator.models.BankResult;
import com.google.gson.Gson;
import com.google.gson.JsonSyntaxException;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.ConsumerCancelledException;
import com.rabbitmq.client.QueueingConsumer;
import com.rabbitmq.client.ShutdownSignalException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Future;
import lb_aggregator.Dictionary;
import lb_aggregator.channels.Producer;

public class Initializer implements Runnable {

    Gson gson = new Gson();
    ExecutorService threadExecutor;
    CountDownHandler cdh;
    Producer p;

    public Initializer(ExecutorService es, Producer p, CountDownHandler cdh) {
        this.threadExecutor = es;
        this.cdh = cdh;
        this.p = p;
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

            System.out.println("Initializer running");
            while (true) {
                // When we get a notification from the recipient list, we set an entry in the dict.
                // It contains the SSN, and the amount of banks we're expecting quotes from.
                // The consumer uses this to determine where to store the responses, and when to return a quote prematurely.
                QueueingConsumer.Delivery delivery = consumer.nextDelivery();
                String message = new String(delivery.getBody());
                InitObject iob = gson.fromJson(message, InitObject.class);
                
                Dictionary.dictionary.put(iob.getSsn(), new BankResult(iob.getBankAmount(), new ArrayList<BankResponse>()));
                System.out.println("Starting new countdown thread");
                
                Future f = threadExecutor.submit(new CountDown(iob.getSsn(), p));
                cdh.addThread(iob.getSsn(), f);
            }

        } catch (JsonSyntaxException | ConsumerCancelledException | ShutdownSignalException | IOException | InterruptedException e) {

        }
    }

}
