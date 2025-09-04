from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Student
from .forms import StudentForm

def student_list(request):
    """
    Display list of all students with search and pagination
    """
    # Get search query from GET parameters
    search_query = request.GET.get('search', '')
    
    # Filter students based on search query
    students = Student.objects.all()
    if search_query:
        students = students.filter(
            Q(name__icontains=search_query) |
            Q(course__icontains=search_query) |
            Q(year_level__icontains=search_query)
        )
    
    # Pagination - 10 students per page
    paginator = Paginator(students, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'total_students': Student.objects.count(),
    }
    return render(request, 'students/student_list.html', context)

def student_create(request):
    """
    Create a new student
    """
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'Student "{student.name}" has been created successfully!')
            return redirect('student_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentForm()
    
    context = {
        'form': form,
        'title': 'Add New Student',
        'button_text': 'Add Student'
    }
    return render(request, 'students/student_form.html', context)

def student_update(request, pk):
    """
    Update an existing student
    """
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'Student "{student.name}" has been updated successfully!')
            return redirect('student_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentForm(instance=student)
    
    context = {
        'form': form,
        'student': student,
        'title': 'Edit Student',
        'button_text': 'Update Student'
    }
    return render(request, 'students/student_form.html', context)

def student_delete(request, pk):
    """
    Delete a student with confirmation
    """
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        student_name = student.name
        student.delete()
        messages.success(request, f'Student "{student_name}" has been deleted successfully!')
        return redirect('student_list')
    
    context = {
        'student': student
    }
    return render(request, 'students/student_confirm_delete.html', context)

def student_detail(request, pk):
    """
    Display detailed information about a student
    """
    student = get_object_or_404(Student, pk=pk)
    context = {
        'student': student
    }
    return render(request, 'students/student_detail.html', context)