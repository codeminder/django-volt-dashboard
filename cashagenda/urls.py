# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from . import views
from .views import *

urlpatterns = [

    # The home page
    path('', views.dashboard, name='cashagenda_home'),
    path('accounts/', views.accounts, name='cashagenda_accounts'),
    path('budgets/', views.budgets, name='cashagenda_budgets'),
    path('journals/', views.journals, name='cashagenda_journals'),
    
    # path('add_cost/', AddCostView.as_view(), name='cashagenda_add_cost'),
    # path('add_profit/', AddProfitView.as_view(), name='cashagenda_add_profit'),
    
    path('cost/new', CostCreateView.as_view(extra_context = get_page_context("cashagenda_cost_new")), name='cashagenda_cost_new'),
    path('profit/new', ProfitCreateView.as_view(extra_context = get_page_context("cashagenda_profit_new")), name='cashagenda_profit_new'),
    path('transfer/new', TransferCreateView.as_view(extra_context = get_page_context("cashagenda_transfer_new")), name='cashagenda_transfer_new'),
    path('inventory/new', InventoryCreateView.as_view(extra_context = get_page_context("cashagenda_inventory_new")), name='cashagenda_inventory_new'),
    path('currencyexchange/new', CurrencyExchangeCreateView.as_view(extra_context = get_page_context("cashagenda_currencyexchange_new")), name='cashagenda_currencyexchange_new'),
    
    path('cost/edit/<int:pk>/', CostUpdateView.as_view(extra_context = get_page_context("cashagenda_cost_update")), name='cashagenda_cost_update'),
    path('profit/edit/<int:pk>/', ProfitUpdateView.as_view(extra_context = get_page_context("cashagenda_profit_update")), name='cashagenda_profit_update'),
    path('transfer/edit/<int:pk>/', TransferUpdateView.as_view(extra_context = get_page_context("cashagenda_transfer_update")), name='cashagenda_transfer_update'),
    path('inventory/edit/<int:pk>/', InventoryUpdateView.as_view(extra_context = get_page_context("cashagenda_inventory_update")), name='cashagenda_inventory_update'),
    path('currencyexchange/edit/<int:pk>/', CurrencyExchangeUpdateView.as_view(extra_context = get_page_context("cashagenda_currencyexchange_update")), name='cashagenda_currencyexchange_update'),
    # path('example/', views.example_form),
    path('ajax/getbalance/', views.get_ajax_account_balance, name='cashagenda_ajax_getbalance'),

]