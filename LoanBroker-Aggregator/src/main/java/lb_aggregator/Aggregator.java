/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package lb_aggregator;

import lb_aggregator.threads.Initializer;
import java.io.IOException;

import com.rabbitmq.client.ConnectionFactory;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import lb_aggregator.channels.Consumer;
import lb_aggregator.channels.Producer;
import lb_aggregator.threads.CountDownHandler;

public class Aggregator {

    public static void main(String[] args) throws IOException, Exception {
        
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost("localhost");

        ExecutorService threadExecutor = Executors.newCachedThreadPool();
        
        Producer p = new Producer();
        CountDownHandler cdh = new CountDownHandler();
        
        // Starting up the Initializer in its own thread, letting it consumes notifications from the recipient list.
        threadExecutor.execute(new Initializer(threadExecutor, p, cdh));
        
        // Starting up the Consumer, which consumes responses from the normalizer.
        Consumer consumer = new Consumer(p, cdh);

        consumer.consume();
    }
}
