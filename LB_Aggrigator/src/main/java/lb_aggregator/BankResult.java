
package lb_aggregator;

import java.util.ArrayList;


public class BankResult {

        int i;
        ArrayList<BankResponse> a;
        
        public BankResult(int i, ArrayList a) {
            this.i = i;
            this.a = a;
        }

        public int getI() {
            return i;
        }

        public void setI(int i) {
            this.i = i;
        }

        public void setA(ArrayList<BankResponse> a) {
            this.a = a;
        }

        public ArrayList<BankResponse> getA() {
            return a;
        }
    
}
