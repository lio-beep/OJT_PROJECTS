from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import (
    ListView, DetailView, CreateView, 
    UpdateView, DeleteView
)
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import JournalEntry
from .forms import JournalEntryForm

class JournalEntryListView(LoginRequiredMixin, ListView):
    model = JournalEntry
    template_name = 'journal/home.html'
    context_object_name = 'entries'
    paginate_by = 6
    
    def get_queryset(self):
        queryset = JournalEntry.objects.filter(author=self.request.user)
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(tags__icontains=search_query)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context

class JournalEntryDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = JournalEntry
    template_name = 'journal/detail.html'
    context_object_name = 'entry'
    
    def test_func(self):
        entry = self.get_object()
        return self.request.user == entry.author

class JournalEntryCreateView(LoginRequiredMixin, CreateView):
    model = JournalEntry
    form_class = JournalEntryForm
    template_name = 'journal/create.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Journal entry created successfully!')
        return super().form_valid(form)

class JournalEntryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = JournalEntry
    form_class = JournalEntryForm
    template_name = 'journal/create.html'
    
    def test_func(self):
        entry = self.get_object()
        return self.request.user == entry.author
    
    def form_valid(self, form):
        messages.success(self.request, 'Journal entry updated successfully!')
        return super().form_valid(form)

class JournalEntryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = JournalEntry
    template_name = 'journal/delete.html'
    success_url = reverse_lazy('journal:home')
    context_object_name = 'entry'
    
    def test_func(self):
        entry = self.get_object()
        return self.request.user == entry.author
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Journal entry deleted successfully!')
        return super().delete(request, *args, **kwargs)

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('journal:home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})