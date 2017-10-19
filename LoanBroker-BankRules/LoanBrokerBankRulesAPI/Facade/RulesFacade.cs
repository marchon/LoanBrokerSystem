using BankRulesAPI.Model;
using Newtonsoft.Json;

namespace BankRulesAPI.Facade
{
    public class RulesFacade
    {
        public string CheckRules(int creditScore, int amount)
        {
            BankAnswer answer = new BankAnswer(
                BankOne(),
                BankTwo(creditScore, amount),
                BankThree(creditScore),
                BankFour(creditScore, amount)
            );

            // Converts the answer to json and returns it.
            return JsonConvert.SerializeObject(answer);
        }

        /// <summary>
        /// Bank 1 will take any loans
        /// </summary>
        /// <returns></returns>
        private bool BankOne()
        {
            return true;
        }

        /// <summary>
        /// Bank 2 will take any loans under 20000, or any loans where the credit score is above 200.
        /// </summary>
        /// <param name="creditScore"></param>
        /// <param name="amount"></param>
        /// <returns></returns>
        private bool BankTwo(int creditScore, int amount)
        {
            return amount < 20000 || creditScore > 200;
        }

        /// <summary>
        /// Bank 3 will take any loans where the credit score is above 400.
        /// </summary>
        /// <param name="creditScore"></param>
        /// <returns></returns>
        private bool BankThree(int creditScore)
        {
            return creditScore > 400;
        }

        /// <summary>
        /// Bank 4 will take any loans where credit score is above 600, or loans where credit score is above 400 and the loan amount is less than 50000.
        /// </summary>
        /// <param name="creditScore"></param>
        /// <param name="amount"></param>
        /// <returns></returns>
        private bool BankFour(int creditScore, int amount)
        {
            return (creditScore > 400 && amount < 50000) || creditScore > 600;
        }

    }
}
