from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    """
    Form for creating and updating student information
    """
    class Meta:
        model = Student
        fields = ['name', 'age', 'course', 'year_level']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter student name',
                'required': True
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter age',
                'min': '16',
                'max': '100',
                'required': True
            }),
            'course': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter course name',
                'required': True
            }),
            'year_level': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
        }
    
    def clean_age(self):
        """Custom validation for age field"""
        age = self.cleaned_data.get('age')
        if age and (age < 16 or age > 100):
            raise forms.ValidationError("Age must be between 16 and 100.")
        return age
    
    def clean_name(self):
        """Custom validation for name field"""
        name = self.cleaned_data.get('name')
        if name and len(name.strip()) < 2:
            raise forms.ValidationError("Name must be at least 2 characters long.")
        return name.strip().title()  # Capitalize properly