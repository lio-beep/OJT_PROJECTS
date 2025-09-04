from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for Student model
    """
    list_display = ['name', 'age', 'course', 'year_level', 'created_at']
    list_filter = ['year_level', 'course', 'created_at']
    search_fields = ['name', 'course']
    list_per_page = 20
    ordering = ['name']
    
    # Fields to display in the form
    fields = ['name', 'age', 'course', 'year_level']
    
    # Read-only fields
    readonly_fields = ['created_at', 'updated_at']
    
    def get_readonly_fields(self, request, obj=None):
        """Make created_at and updated_at readonly in edit mode"""
        if obj:  # Editing an existing object
            return self.readonly_fields + ['created_at', 'updated_at']
        return self.readonly_fields