from django import forms
from .models import Interpretation

class InterpretationForm(forms.ModelForm):


    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Interpretation
        fields = ['text', 'chart', 'obj']