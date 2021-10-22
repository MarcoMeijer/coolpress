from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from press.models import Post, PostStatus, Category


def index(request):
    return HttpResponse("<b>Hello world!</b>")

def get_html_from_post(post):
    return f'''
        <a href="/post/{post.pk}">
            <h1>{post.title}</h1>
        </a>
        <h4>written by {post.author.user.username}</h4>
        <p>{post.body}</p>
        <p>{post.category.label}</p>
        <p>{post.last_update}</p>
    '''

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'post_detail.html', {'post_obj': post})

def posts(request):
    post_list = Post.objects.filter(status=PostStatus.PUBLISHED.value).order_by('-pk')[:10]
    return render(request, 'post_list.html', {'post_list': post_list})

def categories(request):
    categorie_list = Category.objects.all()
    return render(request, 'categories.html', {'category_list': categorie_list})
