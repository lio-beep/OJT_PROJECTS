from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class JournalEntry(models.Model):
    MOOD_CHOICES = [
        ('happy', '😊 Happy'),
        ('sad', '😢 Sad'),
        ('excited', '🎉 Excited'),
        ('calm', '😌 Calm'),
        ('stressed', '😰 Stressed'),
        ('grateful', '🙏 Grateful'),
        ('thoughtful', '🤔 Thoughtful'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES, blank=True, null=True)
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='journal_entries')
    
    class Meta:
        ordering = ['-date_created']
        verbose_name_plural = "Journal Entries"
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('journal:detail', kwargs={'pk': self.pk})
    
    def get_tags_list(self):
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []