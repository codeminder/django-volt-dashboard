from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse_lazy
from .forms import *
from .models import *
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from .utils import getAccountCurrencyCrossTable
from django.views.generic import DetailView
from .utils import get_page_context, get_aware_datetime
from django.http import JsonResponse


# Create your views here.

@login_required(login_url="/login/")
def dashboard(request):
    
    context = get_page_context("dashboard")

    html_template = loader.get_template('cashagenda/dashboard.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def accounts(request):
    
    context = get_page_context("accounts")

    html_template = loader.get_template('cashagenda/accounts.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def budgets(request):
    
    context = get_page_context("budgets")

    html_template = loader.get_template('cashagenda/budgets.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def journals(request):
    
    context = get_page_context("journals")
    docs = Document.objects.all().select_related("profit", "cost", "transfer", "inventory", 
                                                 "currencyexchange", "currency", "account", 
                                                 "cost__budget", "profit__budget", "inventory__budget",
                                                 "transfer__account_in", 
                                                 "currencyexchange__currency_in", 
                                                #  "currencyexchange__sum_in",
                                                #  "inventory__sum_diff"
                                                 ).order_by("-date", "-pk")
    # for doc in docs:
    #     print(doc)
    context["docs"] = docs

    html_template = loader.get_template('cashagenda/journals.html')
    return HttpResponse(html_template.render(context, request))

# @login_required(login_url="/login/")
# def add_cost(request):
        
#     context = get_page_context("add_cost")
    
#     if request.method == "POST":
#         form = AddCost(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("cashagenda_journals")
#     else:
#         form = AddCost()
        
#     context["form"] = form
    
#     html_template = loader.get_template('cashagenda/add_cost.html')
#     return HttpResponse(html_template.render(context, request))

def example_form(request):
    context ={}
    if request.method == "POST":
        form = ExampleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("cashagenda_journals")
    else:
        form = ExampleForm()
        
    context["form"] = form
    
    html_template = loader.get_template('cashagenda/example.html')
    return HttpResponse(html_template.render(context, request))

def get_ajax_account_balance(request):
    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == "POST":
        # get the data from the client side.
        doc_id = request.GET.get("doc_id", None)
        acc_id = request.GET.get("acc_id", None)
        cur_id = request.GET.get("cur_id", None)
        date_str = request.GET.get("date", None)
        
        if not acc_id or not cur_id:
            return JsonResponse({}, status = 400)
        
        acc = Account.objects.get(pk=acc_id)
        cur = Currency.objects.get(pk=cur_id)
        
        if doc_id:
            doc = Document.objects.get(pk=doc_id)

        if date_str:
            date_str =  
            
        if BalanceRecord.objects.filter(nick_name = nick_name).exists():
            # if nick_name found return not valid new friend
            return JsonResponse({"valid":False}, status = 200)
        else:
            # if nick_name not found, then user can create a new friend.
            return JsonResponse({"valid":True}, status = 200)

    return JsonResponse({}, status = 400)

class DocumentCreateCommon:
    success_url = reverse_lazy("cashagenda_journals")
    # template_name = 'cashagenda/new_doc.html'
    template_name = 'cashagenda/edit_doc_custom.html'
    
class CostCreateView(DocumentCreateCommon, LoginRequiredMixin, CreateView):
    
    form_class = CreateCostForm
    # template_name = 'cashagenda/add_cost.html'
    # success_url = reverse_lazy("cashagenda_journals")
    # extra_context = get_page_context("AddCostView")
    
    # def get_context_data(self):
    #     cdata = super().get_context_data()
    #     cdata.update(get_page_context("AddCostView"))
    #     return cdata
    
    # def get_context_data(self):

    #     return get_page_context("AddCostView")
    
class ProfitCreateView(DocumentCreateCommon, LoginRequiredMixin, CreateView):
    
    form_class = CreateProfitForm
    # template_name = 'cashagenda/add_profit.html'
    
class TransferCreateView(DocumentCreateCommon, LoginRequiredMixin, CreateView):
    
    form_class = CreateTransferForm
    # template_name = 'cashagenda/add_profit.html'
    
class InventoryCreateView(DocumentCreateCommon, LoginRequiredMixin, CreateView):
    
    form_class = CreateInventoryForm
    # template_name = 'cashagenda/add_profit.html'
    
class CurrencyExchangeCreateView(DocumentCreateCommon, LoginRequiredMixin, CreateView):
    
    form_class = CreateCurrencyExchangeForm
    # template_name = 'cashagenda/add_profit.html'


class DocumentUpdateCommon:
    #template_name = 'cashagenda/edit_doc.html'
    template_name = 'cashagenda/edit_doc_custom.html'
    success_url = reverse_lazy("cashagenda_journals")

class CostUpdateView(DocumentUpdateCommon, LoginRequiredMixin, UpdateView):
    
    model = Cost
    # model = Document  
    form_class = CreateCostForm
    # model = AddCostForm.Meta.model
    # template_name = 'cashagenda/edit_doc.html'
    # template_name = 'cashagenda/add_cost.html'
    # def __init__(self, extra_context) -> None:
    #     super().__init__()
    
class ProfitUpdateView(DocumentUpdateCommon, LoginRequiredMixin, UpdateView):
     
    model = Profit
    form_class = CreateProfitForm
    
class TransferUpdateView(DocumentUpdateCommon, LoginRequiredMixin, UpdateView):
     
    model = Transfer
    form_class = CreateTransferForm
    
class InventoryUpdateView(DocumentUpdateCommon, LoginRequiredMixin, UpdateView):
     
    model = Inventory
    form_class = CreateInventoryForm
    
class CurrencyExchangeUpdateView(DocumentUpdateCommon, LoginRequiredMixin, UpdateView):
     
    model = CurrencyExchange
    form_class = CreateCurrencyExchangeForm
    

