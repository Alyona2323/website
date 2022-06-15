from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
                  path('admin/', admin.site.urls, name="admin"),
                  path('', include("blog.urls")),
                  path('gallery/', include("gallery.urls")),
                  # path('login/', LoginView.as_view(), name="blog_login"),
                  # path('logout/', LogoutView.as_view(), {"next_page": "index"}, name="blog_logout"),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
