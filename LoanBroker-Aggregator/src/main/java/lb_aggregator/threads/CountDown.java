
package lb_aggregator.threads;

import java.util.logging.Level;
import java.util.logging.Logger;
import lb_aggregator.Dictionary;
import lb_aggregator.channels.Producer;
import lb_aggregator.models.BankResponse;

public class CountDown implements Runnable {

    String ssn;
    Producer p;
    public CountDown(String ssn, Producer p) {
        this.ssn = ssn;
        this.p = p;
    }
    
    @Override
    public void run() {
        try {
            // Wait for 30 seconds. If all bank quotes have not been retrieved by that time,
            // just return the best quote out of the ones we have so far.
            Thread.sleep(20000);
            
            
            BankResponse me = Dictionary.checkBestResult(ssn);
            p.publishResult(me.getSsn(),me.getInterest_rate(),me.getBank());
            Dictionary.dictionary.remove(ssn);
            
            System.out.println("Countdown thread reached eol, shutting down");
        } catch (InterruptedException ex) {
            System.out.println("Countdown terminated.");
        }
    }
    
}
