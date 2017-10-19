namespace BankRulesAPI.Model
{
    public class BankAnswer
    {
        public bool Bank1 { get; set; }
        public bool Bank2 { get; set; }
        public bool Bank3 { get; set; }
        public bool Bank4 { get; set; }

        public BankAnswer(bool bank1, bool bank2, bool bank3, bool bank4)
        {
            Bank1 = bank1;
            Bank2 = bank2;
            Bank3 = bank3;
            Bank4 = bank4;
        }
    }
}
