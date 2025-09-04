from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field
from .models import Post, Comment

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-3'),
                Column('last_name', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Field('username', css_class='form-group mb-3'),
            Field('email', css_class='form-group mb-3'),
            Field('password1', css_class='form-group mb-3'),
            Field('password2', css_class='form-group mb-3'),
            Submit('submit', 'Create Account', css_class='btn btn-primary-custom w-100')
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'categories', 'status']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('title', css_class='form-group mb-3'),
            Field('content', css_class='form-group mb-3'),
            Field('categories', css_class='form-group mb-3'),
            Field('status', css_class='form-group mb-3'),
            Submit('submit', 'Save Post', css_class='btn btn-primary-custom')
        )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author_name', 'author_email', 'body']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Your Comment'}),
            'author_name': forms.TextInput(attrs={'placeholder': 'Your Name'}),
            'author_email': forms.EmailInput(attrs={'placeholder': 'Your Email'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('author_name', css_class='form-group col-md-6 mb-3'),
                Column('author_email', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Field('body', css_class='form-group mb-3'),
            Submit('submit', 'Post Comment', css_class='btn btn-primary-custom')
        )

class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search posts...',
            'class': 'form-control',
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('query', css_class='form-group col-md-10'),
                Column(Submit('submit', 'Search', css_class='btn btn-custom'), css_class='col-md-2'),
                css_class='form-row align-items-end'
            )
        )