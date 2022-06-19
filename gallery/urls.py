from django.urls import path
from .views import gallery, CreatePhotoView

urlpatterns = [
    path('', gallery, name="gallery"),
    path('upload/', CreatePhotoView.as_view(), name="upload"),
]
