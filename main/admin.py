from django.contrib import admin
from .models import Media

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ['title', 'media_type', 'uploaded_by', 'uploaded_at', 'file']
    list_filter = ['media_type', 'uploaded_by', 'uploaded_at']
    search_fields = ['title', 'description']
    
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()
        self.message_user(request, "Selected media files were deleted successfully")
