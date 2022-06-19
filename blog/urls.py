from django.urls import path
from blog import views
from .views import register_user, CreatePostView, login_view, logout_view, PostComment, DeletePostView, UpdatePostView, CommentUpdateView, DeleteCommentView

urlpatterns = [
    path('ua_online', views.index, name="index"),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('ua_online/about/', views.about, name="about"),
    path('ua_online/post/<int:id>/', views.post, name="post"),
    path('ua_online/category/<int:id>/', views.category, name="category"),
    path('ua_online/search/', views.search, name="search"),
    path('ua_online/create/', CreatePostView.as_view(), name="create"),
    path('ua_online/register/', register_user, name='register'),
    path('ua_online/comment/<int:id>/', PostComment.as_view(), name='comment'),
    path('like/<int:id>/', views.like, name='like'),
    path('ua_online/edit//<int:pk>/', UpdatePostView.as_view(), name='edit'),
    path('ua_online/delete/<int:pk>/', DeletePostView.as_view(), name='delete'),
    path('ua_online/update_comment/<int:pk>/', CommentUpdateView.as_view(), name='update_comment'),
    path('ua_online/delete_comment/<int:pk>/', DeleteCommentView.as_view(), name='delete_comment'),
]
