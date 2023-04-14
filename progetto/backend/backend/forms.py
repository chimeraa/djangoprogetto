from django import forms

class QAForm(forms.Form):
    question = forms.CharField(max_length=255)
    answer = forms.ChoiceField(choices=[(true), ("no", "No")])