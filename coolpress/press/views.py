from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from press.forms import PostForm
from press.models import Category, Post, PostStatus


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

@login_required
def post_update(request, post_id=None):
    post = None
    if post_id:
        post = get_object_or_404(Post, pk=post_id)
        if request.user != post.author.user:
            return HttpResponseBadRequest('Now Allowed to change others posts')
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user.cooluser
            instance.save()
            redirect_url = reverse('post-detail', kwargs={'post_id': instance.id})
            return HttpResponseRedirect(redirect_url)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'post_update.html', {'form': form})
