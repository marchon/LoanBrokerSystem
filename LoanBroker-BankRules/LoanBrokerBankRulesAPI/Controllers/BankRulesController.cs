using Microsoft.AspNetCore.Mvc;
using BankRulesAPI.Facade;

namespace BankRulesAPI.Controllers
{
    [Route("api/[controller]")]
    public class BankRulesController
    {
        private RulesFacade facade = new RulesFacade();

        // Get api/bankrules
        [HttpGet()]
        public string Get()
        {
            return "Bank rules API. To figure out which banks will loan money, write the creditscore, and the amount in the url: Example bankrules/198/2000";
        }
        
        // GET api/bankrules/198/2000
        [HttpGet("{creditscore}/{amount}")]
        public string Get(int creditscore, int amount)
        {
            return facade.CheckRules(creditscore, amount);
        }
    }
}
