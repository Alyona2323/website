from django.urls import path
from .views import gallery, upload

urlpatterns = [
    path('', gallery, name="gallery"),
    path('upload/', upload, name="upload"),
]
