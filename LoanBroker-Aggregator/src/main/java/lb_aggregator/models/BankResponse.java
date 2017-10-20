
package lb_aggregator.models;


public class BankResponse {
    String ssn;
    double interest_rate;
    String bank;

    public BankResponse(String ssn, double interest_rate, String bank) {
        this.ssn = ssn;
        this.interest_rate = interest_rate;
        this.bank = bank;
    }

    public String getSsn() {
        return ssn;
    }

    public void setSsn(String ssn) {
        this.ssn = ssn;
    }

    public double getInterest_rate() {
        return interest_rate;
    }

    public void setInterest_rate(double interest_rate) {
        this.interest_rate = interest_rate;
    }

    public String getBank() {
        return bank;
    }

    public void setBank(String bank) {
        this.bank = bank;
    }
    
    
}
