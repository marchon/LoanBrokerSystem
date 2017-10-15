
package lb_aggregator;

import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.HashMap;


public class Dictionary {
    static HashMap<String,BankResult> dictionary = new HashMap<String,BankResult>();

        
    public static BankResult getFromDictionary(String ssn){
        return dictionary.get(ssn);
    }
    
    public static void setDictionary(String ssn, double interestRate, String bankName) {
        
        dictionary.get(ssn).getA().add(new BankResponse(ssn, interestRate, bankName));
        
    }
    
    public static boolean checkResultAmount(String ssn){
        if(dictionary.get(ssn).getI()==dictionary.get(ssn).getA().size()){
            return true;
        } else
            return false;
    }
    
    public static BankResponse checkBestResult(String ssn){
        BankResult best = getFromDictionary(ssn);
        double low = best.getA().get(0).getInterest_rate();
        BankResponse bestResult = best.getA().get(0);
        
        for (BankResponse a : best.getA()){
            
            if (low > a.getInterest_rate())
            {
                low = a.getInterest_rate();
                bestResult = a;
            }
        }
        
        return bestResult;
    }
}
