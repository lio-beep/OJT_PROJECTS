from django.contrib import admin
from .models import JournalEntry

@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'mood', 'date_created', 'date_updated']
    list_filter = ['mood', 'date_created', 'author']
    search_fields = ['title', 'content', 'tags']
    readonly_fields = ['date_created', 'date_updated']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)