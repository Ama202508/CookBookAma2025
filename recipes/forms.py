# recipes/forms.py
from django import forms
from datetime import datetime
from .models import Recipe

class RecipeForm(forms.ModelForm):
    added_at = forms.CharField(
        required=False,
        help_text="Format: YYYY-MM-DD HH:MM:SS (sau YYYY-MM-DD HH:MM / YYYY-MM-DD). Gol = acum."
    )

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'cook_time', 'date_added_str', 'image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*'})
        }

    def clean_added_at(self):
        data = (self.cleaned_data.get('date_added_at') or '').strip()
        if not data:
            return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        formats = ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d']
        for fmt in formats:
            try:
                return datetime.strptime(data, fmt).strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                continue
        raise forms.ValidationError('Format invalid. Folosește YYYY-MM-DD HH:MM[:SS] sau doar data.')

from django.contrib.auth.forms import AuthenticationForm

class MyAuthForm(AuthenticationForm):
    error_messages = {
        "invalid_login": "Utilizator sau parolă incorecte. Verifică datele și încearcă din nou.",
        "inactive": "Acest cont este dezactivat.",
    }
