# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from . import views

urlpatterns = [

    # The home page
    path('', views.dashboard, name='cashagenda_home'),
    path('accounts/', views.accounts, name='cashagenda_accounts'),
    path('budgets/', views.budgets, name='cashagenda_budgets'),
    path('journals/', views.journals, name='cashagenda_journals'),
    path('add_cost/', views.add_cost, name='cashagenda_add_cost'),

]