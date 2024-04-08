from django.contrib import admin
from .models import Photo

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'uploaded_by', 'upload_date', 'count_field', 'manual_count')
    list_filter = ('upload_date', 'uploaded_by')
    search_fields = ('uploaded_by__username', 'uploaded_by__email', 'count_field', 'manual_count')
    readonly_fields = ('upload_date', 'processed_image',)

    def save_model(self, request, obj, form, change):
        if not obj.uploaded_by_id:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Photo, PhotoAdmin)
