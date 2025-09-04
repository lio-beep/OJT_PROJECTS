from django.urls import path
from . import views

app_name = 'journal'

urlpatterns = [
    path('', views.JournalEntryListView.as_view(), name='home'),
    path('entry/<int:pk>/', views.JournalEntryDetailView.as_view(), name='detail'),
    path('entry/new/', views.JournalEntryCreateView.as_view(), name='create'),
    path('entry/<int:pk>/edit/', views.JournalEntryUpdateView.as_view(), name='update'),
    path('entry/<int:pk>/delete/', views.JournalEntryDeleteView.as_view(), name='delete'),
]