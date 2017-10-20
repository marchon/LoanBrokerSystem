package lb_aggregator.threads;

import java.util.HashMap;
import java.util.concurrent.Future;

public class CountDownHandler {
    
    
    public CountDownHandler() {
        
    }
    
    HashMap<String, Future> threadMap = new HashMap<>();
    
    public void addThread(String ssn, Future cd) {
        threadMap.put(ssn, cd);
    }
    
    public void terminateThread(String ssn) {
        threadMap.get(ssn).cancel(true);
    }
    
}
