from django import forms
from .models import *


class AddCost(forms.ModelForm):
    class Meta:
        model = Cost
        fields = '__all__'