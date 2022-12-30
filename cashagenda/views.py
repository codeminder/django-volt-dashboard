from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

svg_paths = {
    "round_diagramm" : r'<path d="M2 10a8 8 0 018-8v8h8a8 8 0 11-16 0z"></path><path d="M12 2.252A8.014 8.014 0 0117.748 8H12V2.252z"></path>',
    "detailed_list" : r'<path fill-rule="evenodd" d="M5 4a3 3 0 00-3 3v6a3 3 0 003 3h10a3 3 0 003-3V7a3 3 0 00-3-3H5zm-1 9v-1h5v2H5a1 1 0 01-1-1zm7 1h4a1 1 0 001-1v-1h-5v2zm0-4h5V8h-5v2zM9 8H4v2h5V8z" clip-rule="evenodd"></path>',
    "bank_card" : r'<path d="M4 4a2 2 0 00-2 2v1h16V6a2 2 0 00-2-2H4z"></path><path fill-rule="evenodd" d="M18 9H2v5a2 2 0 002 2h12a2 2 0 002-2V9zM4 13a1 1 0 011-1h1a1 1 0 110 2H5a1 1 0 01-1-1zm5-1a1 1 0 100 2h1a1 1 0 100-2H9z" clip-rule="evenodd"></path>',
    "box" : r'<path d="M4 3a2 2 0 100 4h12a2 2 0 100-4H4z"></path><path fill-rule="evenodd" d="M3 8h14v7a2 2 0 01-2 2H5a2 2 0 01-2-2V8zm5 3a1 1 0 011-1h2a1 1 0 110 2H9a1 1 0 01-1-1z" clip-rule="evenodd"></path>',
    "gear" : r'<path fill-rule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd"></path>'
}

def get_page_context(active_page):
    
    menu = [
        {
            "title": "Dashboard", 
            "url_name": "cashagenda_home", 
            "active": active_page == 0, 
            "submenu_items": None, 
            "svg_content": svg_paths["round_diagramm"]
            },
        {
            "title": "Journals", 
            "url_name": "cashagenda_journals", 
            "active": active_page == 1, 
            "submenu_items": None, 
            "svg_content": svg_paths["detailed_list"]
            },
        {
            "title": "Accounts", 
            "url_name": "cashagenda_accounts", 
            "active": active_page == 2, 
            "submenu_items": None, 
            "svg_content": svg_paths["bank_card"]
            },
        {
            "title": "Budgets", 
            "url_name": "cashagenda_budgets", 
            "active": active_page == 3, 
            "submenu_items": None, 
            "svg_content": svg_paths["box"]
            },
        {
            "title": "Proccessors", 
            "url_name": "cashagenda_budgets", 
            "active": active_page == 4, 
            "submenu_items": 
                [
                    {
                        "title": "PB export", 
                        "url_name": "cashagenda_accounts", 
                        "active": active_page == 7
                        },
                    {
                        "title": "Acc Inventory", 
                        "url_name": "cashagenda_budgets", 
                        "active": active_page == 8
                        }                   
                    ], 
            "svg_content": svg_paths["gear"]
            }
    ]
    return {"sidebar_menu": menu}


# Create your views here.

@login_required(login_url="/login/")
def index(request):
    
    context = get_page_context(0)
    context['segment'] =  'index'

    html_template = loader.get_template('cashagenda/dashboard.html')
    # return HttpResponse("Start page app")
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def dashboard(request):
    
    context = get_page_context(0)
    context['segment'] =  'index'

    html_template = loader.get_template('cashagenda/dashboard.html')
    # return HttpResponse("Start page app")
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def accounts(request):
    
    context = get_page_context(2)
    context['segment'] =  'index'

    html_template = loader.get_template('cashagenda/accounts.html')
    # return HttpResponse("Start page app")
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def budgets(request):
    
    context = get_page_context(3)
    context['segment'] =  'index'

    html_template = loader.get_template('cashagenda/budgets.html')
    # return HttpResponse("Start page app")
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def journals(request):
    
    context = get_page_context(1)
    context['segment'] =  'index'

    html_template = loader.get_template('cashagenda/journals.html')
    # return HttpResponse("Start page app")
    return HttpResponse(html_template.render(context, request))
