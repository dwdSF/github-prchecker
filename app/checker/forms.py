from django import forms


class CheckForm(forms.Form):

    username = forms.CharField(max_length=50, required=True)
