package lb_aggregator;

import lb_aggregator.models.BankResponse;
import lb_aggregator.models.BankResult;
import java.util.HashMap;

public class Dictionary {

    public static HashMap<String, BankResult> dictionary = new HashMap<String, BankResult>();

    public static BankResult getFromDictionary(String ssn) {
        return dictionary.get(ssn);
    }

    public static void setDictionary(String ssn, double interestRate, String bankName) {

        dictionary.get(ssn).getA().add(new BankResponse(ssn, interestRate, bankName));

    }

    public static boolean checkResultAmount(String ssn) {
        return dictionary.get(ssn).getI() == dictionary.get(ssn).getA().size();
    }

    public static BankResponse checkBestResult(String ssn) {
        BankResult best = getFromDictionary(ssn);
        BankResponse bestResult;
        if (!best.getA().isEmpty()) {
            double low = best.getA().get(0).getInterest_rate();
            bestResult = best.getA().get(0);

            for (BankResponse a : best.getA()) {

                if (low > a.getInterest_rate()) {
                    low = a.getInterest_rate();
                    bestResult = a;
                }
            }
        } else {
            bestResult = new BankResponse(ssn, 0, "No banks returned a response. Your loan may be too undesirable.");
        }

        return bestResult;
    }
}
