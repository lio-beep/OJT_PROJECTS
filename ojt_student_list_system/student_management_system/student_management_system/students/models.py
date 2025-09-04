from django.db import models
from django.urls import reverse

class Student(models.Model):
    """
    Student model representing a student with basic information
    """
    # Choices for year level
    YEAR_CHOICES = [
        ('1', 'First Year'),
        ('2', 'Second Year'),
        ('3', 'Third Year'),
        ('4', 'Fourth Year'),
    ]
    
    name = models.CharField(max_length=100, help_text="Student's full name")
    age = models.PositiveIntegerField(help_text="Student's age")
    course = models.CharField(max_length=100, help_text="Course/Program name")
    year_level = models.CharField(
        max_length=1, 
        choices=YEAR_CHOICES, 
        help_text="Current year level"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']  # Order students by name
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
    
    def __str__(self):
        return f"{self.name} - {self.course} (Year {self.year_level})"
    
    def get_absolute_url(self):
        """Return the URL for student detail view"""
        return reverse('student_detail', kwargs={'pk': self.pk})