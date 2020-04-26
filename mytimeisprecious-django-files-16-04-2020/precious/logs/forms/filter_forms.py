from django import forms


class TagsFilterForm(forms.Form):

    employer = forms.CharField(required=False)
    tags = forms.CharField(max_length=50, required=False)