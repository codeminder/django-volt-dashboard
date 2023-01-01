from django import forms
from .models import *


class AddCost(forms.ModelForm):
    class Meta:
        model = Cost
        fields = '__all__'
        widgets = {
            'date': forms.DateTimeInput(attrs={
                'class': 'form-control datepicker-input', 
                'placeholder': 'YYYY-MM-DD hh:mm:ss',
                'required': 'required'}),
            'account': forms.Select(attrs={
                'class': 'form-select', 
                'required': 'required'}),
            'sum': forms.NumberInput({
                'class': 'form-control', 
                'required': 'required',
                'step': '0.01'}), 
            'currency': forms.Select(attrs={
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