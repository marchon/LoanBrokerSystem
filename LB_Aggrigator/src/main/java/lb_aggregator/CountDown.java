
package lb_aggregator;

import java.util.logging.Level;
import java.util.logging.Logger;

public class CountDown implements Runnable {

    String ssn;
    public CountDown(String ssn) {
        this.ssn = ssn;
    }

    
    @Override
    public void run() {
        try {
            Thread.sleep(30000);
            
            BankResult answer = Dictionary.getFromDictionary(ssn);
                    
        } catch (InterruptedException ex) {
            Logger.getLogger(CountDown.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
    
}
