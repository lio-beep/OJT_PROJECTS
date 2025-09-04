from django import forms
from .models import JournalEntry

class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ['title', 'content', 'mood', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter a title...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Write your thoughts...', 
                'rows': 8
            }),
            'mood': forms.Select(attrs={'class': 'form-select'}),
            'tags': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'work, personal, travel...'
            }),
        }