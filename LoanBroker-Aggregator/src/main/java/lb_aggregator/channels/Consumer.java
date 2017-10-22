package lb_aggregator.channels;

import lb_aggregator.models.BankResponse;
import com.google.gson.Gson;
import com.google.gson.JsonSyntaxException;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.ConsumerCancelledException;
import com.rabbitmq.client.QueueingConsumer;
import com.rabbitmq.client.ShutdownSignalException;
import java.io.IOException;
import lb_aggregator.Dictionary;
import lb_aggregator.threads.CountDownHandler;

public class Consumer {

    public Consumer(Producer p, CountDownHandler cdh) {
        this.p = p;
        this.cdh = cdh;
    }

    Producer p;
    CountDownHandler cdh;
    Gson gson = new Gson();

    public void consume() {
        try {
            // Setting up the channel that the normalizer publishes loan quotes to.
            ConnectionFactory factory = new ConnectionFactory();
            factory.setHost("localhost");
            Connection connection = factory.newConnection();
            Channel channel = connection.createChannel();

            channel.queueDeclare("g6_queue_aggregator", false, false, false, null);
            QueueingConsumer consumer = new QueueingConsumer(channel);
            channel.basicConsume("g6_queue_aggregator", true, consumer);

            System.out.println("Consumer running");
            while (true) {
                // When receiving a loan quote from the normalizer, we cast it to an object.
                // We then add it to the dict by using the SSN provided.
                QueueingConsumer.Delivery delivery = consumer.nextDelivery();
                String message = new String(delivery.getBody());
                BankResponse bankResponse = gson.fromJson(message, BankResponse.class);
                System.out.println("Got response from " + bankResponse.getBank() + " for the SSN " + bankResponse.getSsn());
                if (Dictionary.dictionary.containsKey(bankResponse.getSsn())) {
                    // If we have retrieved all loan quotes required for a specific SSN,
                    // we halt the countdown, and return the result to the user immediately.
                    Dictionary.dictionary.get(bankResponse.getSsn()).getA().add(bankResponse);
                    System.out.println(bankResponse.getSsn() + " has amount: " + Dictionary.checkResultAmount(bankResponse.getSsn()));
                    if (Dictionary.checkResultAmount(bankResponse.getSsn())) {
                        BankResponse me = Dictionary.checkBestResult(bankResponse.getSsn());
                        p.publishResult(me.getSsn(), me.getInterest_rate(), me.getBank());
                        Dictionary.dictionary.remove(bankResponse.getSsn());
                        cdh.terminateThread(bankResponse.getSsn());
                    }
                }
            }

        } catch (JsonSyntaxException | ConsumerCancelledException | ShutdownSignalException | IOException | InterruptedException e) {

        }
    }
}
