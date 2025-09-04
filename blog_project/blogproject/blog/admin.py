from django.contrib import admin
from django.utils.html import format_html
from .models import Post, Comment, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'post_count', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    readonly_fields = ['created_at']

    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Number of Posts'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'created_at', 'category_list']
    list_filter = ['status', 'author', 'created_at', 'categories']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    filter_horizontal = ['categories']
    
    fieldsets = (
        ('Post Information', {
            'fields': ('title', 'slug', 'author', 'status')
        }),
        ('Content', {
            'fields': ('content', 'categories')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']

    def category_list(self, obj):
        return ", ".join([cat.name for cat in obj.categories.all()]) or "No categories"
    category_list.short_description = 'Categories'

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('categories')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'post', 'created_at', 'active_status']
    list_filter = ['active', 'created_at']
    search_fields = ['author_name', 'author_email', 'body']
    actions = ['approve_comments', 'disapprove_comments']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Comment Information', {
            'fields': ('post', 'author_name', 'author_email', 'active')
        }),
        ('Content', {
            'fields': ('body',)
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )

    def active_status(self, obj):
        if obj.active:
            return format_html('<span style="color: green;">✓ Active</span>')
        return format_html('<span style="color: red;">✗ Inactive</span>')
    active_status.short_description = 'Status'

    def approve_comments(self, request, queryset):
        updated = queryset.update(active=True)
        self.message_user(request, f'{updated} comments were approved.')
    approve_comments.short_description = "Approve selected comments"

    def disapprove_comments(self, request, queryset):
        updated = queryset.update(active=False)
        self.message_user(request, f'{updated} comments were disapproved.')
    disapprove_comments.short_description = "Disapprove selected comments"