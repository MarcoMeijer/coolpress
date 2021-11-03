from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:post_id>', views.post_detail, name='post-detail'),
    path('posts/', views.PostList.as_view(), name='posts-list'),
    path('posts/<str:category_slug>', views.CategoryPostList.as_view(), name='post-list-category'),
    path('posts/author/<int:pk>', views.AuthorPostList.as_view(), name='posts-list-author'),
    path('post/add/', views.post_update, name='post-add'),
    path('post/update/<int:post_id>', views.post_update, name='post-update'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('category/<int:pk>/', views.CategoryDetail.as_view(), name='category-detail'),
    path('categories/', views.CategoryList.as_view(), name='category-list'),
    path('category/add/', views.CategoryAdd.as_view(), name='category-add'),
    path('category/update/<int:pk>', views.CategoryUpdate.as_view(), name='category-update'),
    path('category-json/<str:slug>', views.category_api, name='category-json'),
    path('user/<int:pk>', views.CoolUserDetail.as_view(), name='cooluser-detail'),
    path('users/', views.CoolUserList.as_view(), name='cooluser-list'),
    path('posts-filtered/', views.search_ajax, name='search-ajax'),
    path('post-filtered/', views.PostFilteredByText.as_view(), name='post-filtered'),
    path('accounts/', include('django.contrib.auth.urls'), name='accounts'),
]
