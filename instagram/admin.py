from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'instagram_id', 'caption_preview', 'media_type', 'timestamp')
    search_fields = ('instagram_id', 'caption')
    ordering = ('-timestamp',)
    
    def caption_preview(self, obj):
        return obj.caption[:50] + '...' if len(obj.caption) > 50 else obj.caption
    caption_preview.short_description = 'Caption'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'instagram_id', 'post', 'text_preview', 'timestamp')
    search_fields = ('instagram_id', 'text')
    list_filter = ('post',)
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Comment'