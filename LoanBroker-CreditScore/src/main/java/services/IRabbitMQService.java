package services;

import com.rabbitmq.client.AMQP;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.GetResponse;
import java.io.IOException;
import java.util.Map;
import java.util.concurrent.TimeoutException;

/**
 * Interface for the RabbitMQ Service
 * 
 * @author Group 6
 */
public interface IRabbitMQService {
    /**
     * Creates a connection to the RabbitMQ message service.
     * 
     * @param host
     * @param user
     * @param pass
     * @param port
     * @return
     * @throws IOException
     * @throws TimeoutException 
     */
    public Connection getRabbitMQConnection(String host, String user, String pass, int port) throws IOException, TimeoutException;
    /**
     * Creates a connection to the RabbitMQ message service. Use this to connect to localhost.
     * 
     * @param host
     * @return
     * @throws IOException
     * @throws TimeoutException 
     */
    public Connection getRabbitMQConnection(String host) throws IOException, TimeoutException;
    /**
     * Function for creating a queue. If the queue already exist no action is taken.
     * 
     * @param queueName
     * @param durable
     * @param exclusive
     * @param autoDelete
     * @param args
     * @param channel
     * @throws IOException 
     */
    public void createQueue(String queueName, boolean durable, boolean exclusive, boolean autoDelete, Map<String, Object> args, Channel channel) throws IOException;
    /**
     * Function to remove a queue from the RabbitMQ Service.
     * 
     * @param queueName
     * @param channel
     * @throws IOException 
     */
    public void deleteQueue(String queueName, Channel channel) throws IOException;
    /**
     * Function for creating an exchange to communicate with the a queue. If the exchange
     * already exists no action is taken.
     * 
     * @param exchangeName
     * @param exchangeType
     * @param durable
     * @param channel
     * @throws IOException 
     */
    public void createExchange(String exchangeName, String exchangeType, boolean durable, Channel channel) throws IOException;
    /**
     * Function to remove an exchange from the RabbitMQ service.
     * 
     * @param exchangeName
     * @param channel
     * @throws IOException 
     */
    public void deleteExchange(String exchangeName, Channel channel) throws IOException;
    /**
     * Function for binding an exchange to a queue, a routing key is used to provide specific communication routes.
     * 
     * @param exchangeName
     * @param queueName
     * @param routingKey
     * @param channel
     * @throws IOException 
     */
    public void bindExchangeQueue(String exchangeName, String queueName, String routingKey, Channel channel) throws IOException;
    /**
     * Post a message to a queue using a specific exchange and route key. The BasicProperties is to supply headers
     * and other meta data.
     * 
     * @param message
     * @param exchangeName
     * @param routingKey
     * @param props
     * @param channel
     * @throws IOException
     */
    public void postToQueue(String message, String exchangeName, String routingKey, AMQP.BasicProperties props, Channel channel) throws IOException;
    /**
     * Function that retrieves a message from a queue. The autoAcknowledge indicates if the
     * message should be instantly deleted from the queue or hidden until acknowledge is manually
     * send.
     * 
     * @param queueName
     * @param routingKey
     * @param autoAcknowledge
     * @param channel
     * @return
     * @throws IOException 
     */
    public GetResponse getResponseFromQueue(String queueName, String routingKey, boolean autoAcknowledge, Channel channel) throws IOException;
    /**
     * Function to send acknowledge to queue when a message is correctly handled by the service.
     * This is to ensure that a message is not lost without being correctly handled.
     * 
     * @param channel
     * @param response
     * @throws IOException 
     */
    public void sendAcknowledgement(Channel channel, GetResponse response) throws IOException;
    /**
     * Close the RabbitMQ connection.
     * 
     * @param conn
     * @throws IOException
     * @throws TimeoutException 
     */
    public void closeConnection(Connection conn) throws IOException, TimeoutException;
    /**
     * Close the channel.
     * 
     * @param channel
     * @throws IOException
     * @throws TimeoutException 
     */
    public void closeChannel(Channel channel) throws IOException, TimeoutException;
}
