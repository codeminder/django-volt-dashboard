from django import forms
from .models import *

from .widget import DatePickerInput, TimePickerInput, DateTimePickerInput, MinimalSplitDateTimeMultiWidget

class ExampleForm(forms.Form):
        my_date_field = forms.DateField(widget=DatePickerInput)
        my_time_field = forms.TimeField(widget=TimePickerInput)
        my_date_time_field = forms.DateTimeField(widget=DateTimePickerInput)

class CostProfitMetaTemplate:
        # fields = '__all__'
        fields = ('date', 'account', 'sum', 'currency', 'comment', 'budget', 'photo',)
        widgets = {
            'date': MinimalSplitDateTimeMultiWidget(attrs={   #forms.DateTimeInput
                'class': 'form-control datepicker-input', 
                # 'placeholder': 'YYYY-MM-DD hh:mm:ss',
                'required': 'required'}),
            'account': forms.Select(attrs={
                'class': 'form-select', 
                'required': 'required'}),
            'account_in': forms.Select(attrs={
                'class': 'form-select', 
                'required': 'required'}),
            'sum': forms.NumberInput({
                'class': 'form-control', 
                'required': 'required',
                'step': '0.01'}),
            'sum_diff': forms.NumberInput({
                'class': 'form-control', 
                'required': 'required',
                'step': '0.01'}),
            'sum_in': forms.NumberInput({
                'class': 'form-control', 
                'required': 'required',
                'step': '0.01'}), 
            'currency': forms.Select(attrs={
                'class': 'form-select', 
                'required': 'required'}),
            'currency_in': forms.Select(attrs={
                'class': 'form-select', 
                'required': 'required'}),
            'comment': forms.Textarea({
                'class': 'form-control'
                }),
            'budget': forms.Select(attrs={
                'class': 'form-select', 
                'required': 'required'}),
            'photo': forms.FileInput(attrs={
                'class': 'form-control'}),
        }

class CreateCostForm(forms.ModelForm):
    class Meta(CostProfitMetaTemplate):
        model = Cost
        
class CreateProfitForm(forms.ModelForm):
    class Meta(CostProfitMetaTemplate):
        model = Profit
        
class CreateTransferForm(forms.ModelForm):
    class Meta(CostProfitMetaTemplate):
        fields = ('date', 'account', 'account_in', 'sum', 'currency', 'comment', 'photo',)
        model = Transfer
        
class CreateInventoryForm(forms.ModelForm):
    class Meta(CostProfitMetaTemplate):
        fields = ('date', 'account', 'sum', 'sum_diff', 'currency', 'comment', 'budget', 'photo',)
        model = Inventory
        
class CreateCurrencyExchangeForm(forms.ModelForm):
    class Meta(CostProfitMetaTemplate):
        fields = ('date', 'account', 'sum', 'sum_in', 'currency', 'currency_in', 'comment', 'photo',)
        model = CurrencyExchange