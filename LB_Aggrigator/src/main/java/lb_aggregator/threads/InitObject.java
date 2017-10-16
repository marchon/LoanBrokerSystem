package lb_aggregator.threads;

public class InitObject {

    String ssn;
    int bankAmount;

    public InitObject(String ssn, int bankAmount) {
        this.ssn = ssn;
        this.bankAmount = bankAmount;
    }

    public String getSsn() {
        return ssn;
    }

    public void setSsn(String ssn) {
        this.ssn = ssn;
    }

    public int getBankAmount() {
        return bankAmount;
    }

    public void setBankAmount(int bankAmount) {
        this.bankAmount = bankAmount;
    }

}
