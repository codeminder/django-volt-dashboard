from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

svg_paths = {
    "round_diagramm" : ""
}

def get_page_context(active_page):
    
    menu = [
        {"title": "", "url_name": "cashagenda_home", "active": active_page == 0, "submenu_items": None, "svg_content": ""},
        {"title": "Journals", "url_name": "cashagenda_journals", "active": active_page == 1, "submenu_items": None, "svg_content": ""},
        {"title": "Accounts", "url_name": "cashagenda_accounts", "active": active_page == 2, "submenu_items": None, "svg_content": ""},
        {"title": "Budgets", "url_name": "cashagenda_budgets", "active": active_page == 3, "submenu_items": None, "svg_content": ""}
        {"title": "", "url_name": "cashagenda_budgets", "active": active_page == 4, "submenu_items": None, "svg_content": ""}
    ]


# Create your views here.

@login_required(login_url="/login/")
def index(request):
    
    context = get_page_context("index"){'segment': 'index'}

    html_template = loader.get_template('cashagenda/dashboard.html')
    # return HttpResponse("Start page app")
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def dashboard(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('cashagenda/dashboard.html')
    # return HttpResponse("Start page app")
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def accounts(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('cashagenda/accounts.html')
    # return HttpResponse("Start page app")
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def budgets(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('cashagenda/budgets.html')
    # return HttpResponse("Start page app")
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def journals(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('cashagenda/journals.html')
    # return HttpResponse("Start page app")
    return HttpResponse(html_template.render(context, request))
