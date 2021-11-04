from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView

from press.forms import PostForm, CategoryForm
from press.models import Category, Post, PostStatus, CoolUser


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

class AboutView(TemplateView):
    template_name = "about.html"

class CategoryDetail(DetailView):
    model = Category

class CategoryList(ListView):
    model = Category

class CategoryAdd(CreateView):
    model = Category
    form_class = CategoryForm

class CategoryUpdate(UpdateView):
    model = Category
    form_class = CategoryForm

class PostList(ListView):
    model = Post
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'post_list.html'

class CategoryPostList(PostList):
    def get_queryset(self):
        queryset = super(CategoryPostList, self).get_queryset()
        category_slug = self.kwargs['category_slug']
        category = get_object_or_404(Category, slug=category_slug)
        return queryset.filter(category=category)

class AuthorPostList(PostList):
    def get_queryset(self):
        queryset = super(AuthorPostList, self).get_queryset()
        pk = self.kwargs['pk']
        author = get_object_or_404(CoolUser, pk=pk)
        return queryset.filter(author=author)

class PostFilteredByText(PostList):
    def get_queryset(self):
        queryset = super(PostFilteredByText, self).get_queryset()
        search_text = self.request.GET.get('q')
        qs1 = Q(title__icontains=search_text)
        qs2 = Q(body__icontains=search_text)
        qs3 = Q(author__user__username__icontains=search_text)
        qs4 = Q(category__label__icontains=search_text)
        return queryset.filter(qs1 | qs2 | qs3 | qs4)

    def get_context_data(self, *args, **kwargs):
        context = super(PostFilteredByText, self).get_context_data(*args, **kwargs)
        context['search_data'] = self.request.GET.get('q')
        return context

def category_api(request, slug):
    cat = get_object_or_404(Category, slug=slug)
    return JsonResponse(
        dict(slug=cat.slug, label=cat.label)
    )


def search_ajax(request):
    query_search = request.GET.get('q')
    posts = Post.objects.filter(title__icontains=query_search).values('id', 'title', 'body',
                                                                      'author__user__username',
                                                                      'category__label')
    ret = {p['id']: p for p in posts}
    return JsonResponse(
        ret
    )


class CoolUserDetail(DetailView):
    model = CoolUser


class CoolUserList(ListView):
    model = CoolUser
