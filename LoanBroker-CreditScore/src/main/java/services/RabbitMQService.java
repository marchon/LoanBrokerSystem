package services;

import com.rabbitmq.client.AMQP.BasicProperties;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.GetResponse;
import java.io.IOException;
import java.util.Map;
import java.util.concurrent.TimeoutException;

/**
 * *
 * RabbitMQ service.
 *
 * @author Group 6
 */
public class RabbitMQService implements IRabbitMQService {

    @Override
    public Connection getRabbitMQConnection(String host, String user, String pass, int port) throws IOException, TimeoutException {
        ConnectionFactory factory = new ConnectionFactory();
        factory.setUsername(user);
        factory.setPassword(pass);
        factory.setHost(host);
        factory.setPort(port);
        return factory.newConnection();
    }
    
    @Override
    public Connection getRabbitMQConnection(String host) throws IOException, TimeoutException {
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost(host);
        return factory.newConnection();
    }
    
    @Override
    public void createQueue(String queueName, boolean durable, boolean exclusive, boolean autoDelete, Map<String, Object> args, Channel channel) throws IOException {
        channel.queueDeclare(queueName, durable, exclusive, autoDelete, args);
    }
    
    @Override
    public void deleteQueue(String queueName, Channel channel) throws IOException {
        channel.queueDelete(queueName);
    }
    
    @Override
    public void createExchange(String exchangeName, String exchangeType, boolean durable, Channel channel) throws IOException {
        channel.exchangeDeclare(exchangeName, exchangeType, durable);
    }
    
    @Override
    public void deleteExchange(String exchangeName, Channel channel) throws IOException {
        channel.exchangeDelete(exchangeName);
    }
    
    @Override
    public void bindExchangeQueue(String exchangeName, String queueName, String routingKey, Channel channel) throws IOException {
        channel.queueBind(exchangeName, queueName, routingKey);
    }
    
    @Override
    public void postToQueue(String message, String exchangeName, String routingKey, BasicProperties props, Channel channel) throws IOException {
        byte[] messageBytes = message.getBytes();
        channel.basicPublish(exchangeName, routingKey, props, messageBytes);
    }

    @Override
    public GetResponse getResponseFromQueue(String queueName, String routingKey, boolean autoAcknowledge, Channel channel) throws IOException {
        GetResponse response = channel.basicGet(queueName, autoAcknowledge);
        return (response != null) ? response : null;
    }
    
    @Override
    public void sendAcknowledgement(Channel channel, GetResponse response) throws IOException {
        channel.basicAck(response.getEnvelope().getDeliveryTag(), false);
    }
    
    @Override
    public void closeConnection(Connection conn) throws IOException, TimeoutException {
        conn.close();
    }

    @Override
    public void closeChannel(Channel channel) throws IOException, TimeoutException {
        channel.close();
    }
}
