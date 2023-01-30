from django.db.models.functions import Cast
from django.db.models import Sum, F
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_aware, make_aware
from .models import BalanceRecord

svg_paths = {
    "round_diagramm" : r'<path d="M2 10a8 8 0 018-8v8h8a8 8 0 11-16 0z"></path><path d="M12 2.252A8.014 8.014 0 0117.748 8H12V2.252z"></path>',
    "detailed_list" : r'<path fill-rule="evenodd" d="M5 4a3 3 0 00-3 3v6a3 3 0 003 3h10a3 3 0 003-3V7a3 3 0 00-3-3H5zm-1 9v-1h5v2H5a1 1 0 01-1-1zm7 1h4a1 1 0 001-1v-1h-5v2zm0-4h5V8h-5v2zM9 8H4v2h5V8z" clip-rule="evenodd"></path>',
    "bank_card" : r'<path d="M4 4a2 2 0 00-2 2v1h16V6a2 2 0 00-2-2H4z"></path><path fill-rule="evenodd" d="M18 9H2v5a2 2 0 002 2h12a2 2 0 002-2V9zM4 13a1 1 0 011-1h1a1 1 0 110 2H5a1 1 0 01-1-1zm5-1a1 1 0 100 2h1a1 1 0 100-2H9z" clip-rule="evenodd"></path>',
    "box" : r'<path d="M4 3a2 2 0 100 4h12a2 2 0 100-4H4z"></path><path fill-rule="evenodd" d="M3 8h14v7a2 2 0 01-2 2H5a2 2 0 01-2-2V8zm5 3a1 1 0 011-1h2a1 1 0 110 2H9a1 1 0 01-1-1z" clip-rule="evenodd"></path>',
    "gear" : r'<path fill-rule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd"></path>',
    "page" : r'<path fill-rule="evenodd" d="M2 5a2 2 0 012-2h8a2 2 0 012 2v10a2 2 0 002 2H4a2 2 0 01-2-2V5zm3 1h6v4H5V6zm6 6H5v2h6v-2z" clip-rule="evenodd"></path><path d="M15 7h1a2 2 0 012 2v5.5a1.5 1.5 0 01-3 0V7z"></path>'
}

def get_aware_datetime(date_str):
    ret = parse_datetime(date_str)
    return ensure_aware(ret)

def ensure_aware(date_time):
    if not is_aware(date_time):
        date_time = make_aware(date_time)
    return date_time

def get_page_context(active_page):
    
    context = {}
    sidebar_menu = [
        {
            "title": "Dashboard", 
            "url_name": "cashagenda_home", 
            "active": active_page == "dashboard", 
            "submenu_items": None, 
            "svg_content": svg_paths["round_diagramm"]
            },
        {
            "title": "Journals", 
            "url_name": "cashagenda_journals", 
            "active": active_page == "journals", 
            "submenu_items": None, 
            "svg_content": svg_paths["detailed_list"]
            },
        {
            "title": "Accounts", 
            "url_name": "cashagenda_accounts", 
            "active": active_page == "accounts", 
            "submenu_items": None, 
            "svg_content": svg_paths["bank_card"]
            },
        {
            "title": "Budgets", 
            "url_name": "cashagenda_budgets", 
            "active": active_page == "budgets", 
            "submenu_items": None, 
            "svg_content": svg_paths["box"]
            },
        {
            "title": "Create", 
            "url_name": "", 
            "active": active_page == "create", 
            "submenu_items": 
                [
                    {
                        "title": "Cost", 
                        "url_name": "cashagenda_cost_new", 
                        "active": active_page == "cashagenda_cost_new"
                        },
                    {
                        "title": "Profit", 
                        "url_name": "cashagenda_profit_new", 
                        "active": active_page == "cashagenda_profit_new"
                        },
                    {
                        "title": "Transfer", 
                        "url_name": "cashagenda_transfer_new", 
                        "active": active_page == "cashagenda_transfer_new"
                        }, 
                    {
                        "title": "Inventory", 
                        "url_name": "cashagenda_inventory_new", 
                        "active": active_page == "cashagenda_profit_new"
                        }, 
                    {
                        "title": "CurrencyExchange", 
                        "url_name": "cashagenda_currencyexchange_new", 
                        "active": active_page == "cashagenda_profit_new"
                        },                    
                    ], 
            "svg_content": svg_paths["page"]
            },
        {
            "title": "Proccessors", 
            "url_name": "", 
            "active": active_page == "proccessors", 
            "submenu_items": 
                [
                    {
                        "title": "PB export", 
                        "url_name": "cashagenda_accounts", 
                        "active": active_page == "pb_export"
                        },
                    {
                        "title": "Acc Inventory", 
                        "url_name": "cashagenda_budgets", 
                        "active": active_page == "acc_inventory"
                        }                   
                    ], 
            "svg_content": svg_paths["gear"]
            }
    ]
    context["sidebar_menu"] = sidebar_menu
    
    if active_page == "cashagenda_cost_new":
        context["form_action"] = "cashagenda_cost_new"
        context["variant"] = "new"
        context["page_title"] = "New cost"
    elif active_page == "cashagenda_profit_new":
        context["form_action"] = "cashagenda_profit_new"
        context["variant"] = "new"
        context["page_title"] = "New profit"
    elif active_page == "cashagenda_transfer_new":
        context["form_action"] = "cashagenda_transfer_new"
        context["variant"] = "new"
        context["page_title"] = "New transfer"
    elif active_page == "cashagenda_inventory_new":
        context["form_action"] = "cashagenda_inventory_new"
        context["variant"] = "new"
        context["page_title"] = "New inventory"
    elif active_page == "cashagenda_currencyexchange_new":
        context["form_action"] = "cashagenda_currencyexchange_new"
        context["variant"] = "new"
        context["page_title"] = "New currency exchange"
    elif active_page == "cashagenda_cost_update":
        context["form_action"] = "cashagenda_cost_update"
        context["variant"] = "edit"
        context["page_title"] = "Update cost"
    elif active_page == "cashagenda_profit_update":
        context["form_action"] = "cashagenda_profit_update"
        context["variant"] = "edit"
        context["page_title"] = "Update profit"
    elif active_page == "cashagenda_transfer_update":
        context["form_action"] = "cashagenda_transfer_update"
        context["variant"] = "edit"
        context["page_title"] = "Update transfer"
    elif active_page == "cashagenda_inventory_update":
        context["form_action"] = "cashagenda_inventory_update"
        context["variant"] = "edit"
        context["page_title"] = "Update inventory"
    elif active_page == "cashagenda_currencyexchange_update":
        context["form_action"] = "cashagenda_currencyexchange_update"
        context["variant"] = "edit"
        context["page_title"] = "Update currencyexchange"
    elif active_page == "dashboard":
        context["acc_cur_cross_table"] = BalanceRecord.getAccountCurrencyCrossTable()
    
    return context

# def getAccountCurrencyCrossTable():
    
#     accounts = {}
#     currencies = {}
#     аverage_balance = 0
#     basis_for_persent = 0
    
#     dataQS = BalanceRecord.objects.values("account", "account__name", "currency", "currency__name", "currency__course").annotate(
#         cur_sum=Sum("sum"), bal_sum=Sum(F("currency__course")*F("sum")))
    
    
#     for record in dataQS:
        
#         if not accounts.get(record["account"]):
#             accounts[record["account"]] = {}
            
#         accounts[record["account"]]["account"] = record["account"]
#         accounts[record["account"]]["name"] = record["account__name"]
#         accounts[record["account"]][record["currency"]] = {"cur_sum": record["cur_sum"], "bal_sum": record["bal_sum"]}
#         accounts[record["account"]]["acc_sum"] =  accounts[record["account"]].get("acc_sum", 0) + record["bal_sum"] 
        
#         if not currencies.get(record["currency"]):
#             currencies[record["currency"]] = {}
            
#         currencies[record["currency"]]["currency"] = record["currency"]
#         currencies[record["currency"]]["name"] = record["currency__name"]
#         currencies[record["currency"]]["course"] = record["currency__course"]
#         currencies[record["currency"]]["cur_sum"] =  currencies[record["currency"]].get("cur_sum", 0) + record["cur_sum"]
#         currencies[record["currency"]]["bal_sum"] =  currencies[record["currency"]].get("bal_sum", 0) + record["bal_sum"]
        
#         аverage_balance += record["bal_sum"]
#         basis_for_persent = basis_for_persent + record["bal_sum"] if record["bal_sum"] > 0 else 0
    
#     cur_arr = sorted(currencies.values(), key=lambda cur: cur["course"])
#     acc_arr = sorted(accounts.values(), key=lambda acc: -acc["acc_sum"])
    
#     for cur in cur_arr:
#         cur["percent"] = 0        
#         if cur["bal_sum"] > 0 and basis_for_persent > 0:
#             cur["percent"] = round(100 * cur["bal_sum"] / basis_for_persent, 2)
    
#     for acc in acc_arr:
#         acc["currency_sums"] = []
#         for cur in cur_arr:
#             if acc.get(cur["currency"]):
#                 sum = acc[cur["currency"]]["cur_sum"]
#                 bal_sum = acc[cur["currency"]]["bal_sum"]
#                 if cur["course"] > 1:
#                     acc["currency_sums"].append({"bal_sum": bal_sum, "sum_view":f"{sum:.2f} ({bal_sum:.2f})"})
#                 else:
#                     acc["currency_sums"].append({"bal_sum": bal_sum, "sum_view":f"{sum:.2f}"})
#             else:
#                 acc["currency_sums"].append({"bal_sum": 0, "sum_view":"-"})
        
#         acc["percent"] = 0        
#         if acc["acc_sum"] > 0 and basis_for_persent > 0:
#             acc["percent"] = round(100 * acc["acc_sum"] / basis_for_persent, 2) 
    
    
#     return {"accounts": acc_arr, "currencies": cur_arr, "balance": аverage_balance}