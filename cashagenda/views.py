from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

# Create your views here.

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

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
