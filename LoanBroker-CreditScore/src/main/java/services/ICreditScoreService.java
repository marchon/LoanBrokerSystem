package services;

/**
 * Interface for the CreditScoreService
 * 
 * @author Group 6
 */
public interface ICreditScoreService {
    /**
     * Method that returns a credit score from the WDSL Bank SAOP Service.
     * 
     * @param ssn
     * @return int score
     */
    public int getCreditScore(String ssn);
}
