from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # suas outras urls...
    path('photos/', photo_list, name='photo_list'),
    path('upload-photo/', upload_photo, name='upload_photo'),  # URL para o formulário de upload
    path('photos/update/<int:photo_id>/', update_count, name='update_count'),
    path('photos/delete/<int:photo_id>/', delete_photo, name='delete_photo'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)