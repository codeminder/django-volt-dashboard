from .models import BalanceRecord
from django.db.models.functions import Cast
from django.db.models import Sum, F

def getAccountCurrencyCrossTable():
    
    accounts = {}
    currencies = {}
    аverage_balance = 0
    basis_for_persent = 0
    
    dataQS = BalanceRecord.objects.values("account", "account__name", "currency", "currency__name", "currency__course").annotate(
        cur_sum=Sum("sum"), bal_sum=Sum(F("currency__course")*F("sum")))
    
    
    for record in dataQS:
        
        if not accounts.get(record["account"]):
            accounts[record["account"]] = {}
            
        accounts[record["account"]]["account"] = record["account"]
        accounts[record["account"]]["name"] = record["account__name"]
        accounts[record["account"]][record["currency"]] = {"cur_sum": record["cur_sum"], "bal_sum": record["bal_sum"]}
        accounts[record["account"]]["acc_sum"] =  accounts[record["account"]].get("acc_sum", 0) + record["bal_sum"] 
        
        if not currencies.get(record["currency"]):
            currencies[record["currency"]] = {}
            
        currencies[record["currency"]]["currency"] = record["currency"]
        currencies[record["currency"]]["name"] = record["currency__name"]
        currencies[record["currency"]]["course"] = record["currency__course"]
        currencies[record["currency"]]["cur_sum"] =  currencies[record["currency"]].get("cur_sum", 0) + record["cur_sum"]
        currencies[record["currency"]]["bal_sum"] =  currencies[record["currency"]].get("bal_sum", 0) + record["bal_sum"]
        
        аverage_balance += record["bal_sum"]
        basis_for_persent = basis_for_persent + record["bal_sum"] if record["bal_sum"] > 0 else 0
    
    cur_arr = sorted(currencies.values(), key=lambda cur: cur["course"])
    acc_arr = sorted(accounts.values(), key=lambda acc: -acc["acc_sum"])
    
    for cur in cur_arr:
        cur["percent"] = 0        
        if cur["bal_sum"] > 0 and basis_for_persent > 0:
            cur["percent"] = round(100 * cur["bal_sum"] / basis_for_persent, 2)
    
    for acc in acc_arr:
        acc["currency_sums"] = []
        for cur in cur_arr:
            if acc.get(cur["currency"]):
                sum = acc[cur["currency"]]["cur_sum"]
                bal_sum = acc[cur["currency"]]["bal_sum"]
                if cur["course"] > 1:
                    acc["currency_sums"].append({"bal_sum": bal_sum, "sum_view":f"{sum:.2f} ({bal_sum:.2f})"})
                else:
                    acc["currency_sums"].append({"bal_sum": bal_sum, "sum_view":f"{sum:.2f}"})
            else:
                acc["currency_sums"].append({"bal_sum": 0, "sum_view":"-"})
        
        acc["percent"] = 0        
        if acc["acc_sum"] > 0 and basis_for_persent > 0:
            acc["percent"] = round(100 * acc["acc_sum"] / basis_for_persent, 2) 
    
    
    return {"accounts": acc_arr, "currencies": cur_arr, "balance": аverage_balance}