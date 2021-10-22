from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:post_id>', views.post_detail, name='post_detail'),
    path('posts/', views.posts, name='posts')
]
