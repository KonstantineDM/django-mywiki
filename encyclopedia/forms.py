from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import Textarea


class EntryForm(forms.Form):
    """Form for creating new entry"""
    title = forms.CharField(max_length=120, min_length=1, required=True, label="Title")
    entry = forms.CharField(widget=Textarea, required=True, label="Entry")

    def clean_entry(self):
        data = self.cleaned_data["entry"]
        if not data:
            raise ValidationError("Description field can not be empty.")
        else: return data
