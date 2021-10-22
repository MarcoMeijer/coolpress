from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:post_id>', views.post_detail, name='post-detail'),
    path('posts/', views.posts, name='posts'),
    path('categories/', views.categories, name='categories'),
    path('accounts/', include('django.contrib.auth.urls'), name='accounts')
]
