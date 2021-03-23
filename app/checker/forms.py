from django import forms


class GithubProjectForm(forms.Form):

    username = forms.CharField(max_length=50, required=True)
