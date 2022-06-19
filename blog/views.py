from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from rest_framework.reverse import reverse_lazy
from .models import Post, Category, Comment
from .forms import PostForm, CommentForm, UserRegistrationForm, LoginForm
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin


def get_categories():
    all_categories = Category.objects.all()
    return {'cat': all_categories}


def category(request, id=None):
    posts = Post.objects.filter(category__pk=id).order_by("-published_date")
    context = {"posts": posts}
    context.update(get_categories())
    return render(request, "blog/category.html", context)


def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        form = UserRegistrationForm()
        context = {'form': form}
        context.update(get_categories())
    return render(request, 'registration/register.html', context)


def login_view(request):
    form = LoginForm()
    context = {'form': form}
    context.update(get_categories())
    if request.method == 'GET':
        return render(request, 'registration/login.html', context)
    elif request.method == 'POST':
        try:
            user = authenticate(username=request.POST.get('login'),
                                password=request.POST.get('password'))
            if user:
                login(request, user)
        except Exception as e:
            print(e)
            return render(request, 'blog/login.html', {'form': LoginForm(data=request.POST)})
        next = request.GET.get('next', 'index')
        return redirect(next)


def logout_view(request):
    logout(request)
    return redirect("index")


class OnlyForAuthenticatedUsersView(PermissionRequiredMixin, TemplateView):
    permission_required = 'blog.post_confirm_delete'
    template_name = 'registration/secured.html'
    login_url = reverse_lazy('login')
    extra_context = {'title': 'Тільки для авторизованих користувачів!'}


def index(request):
    all_posts = Post.objects.all().order_by("-published_date")
    paginator = Paginator(all_posts, 8)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {'posts': posts, 'page': page}
    context.update(get_categories())
    return render(request, "blog/index.html", context)


def post(request, id=None):
    p = get_object_or_404(Post, pk=id)
    context = {"post": p}
    context.update(get_categories())
    return render(request, "blog/post.html", context)


def about(request):
    p = 'blog/about.html'
    context = {"post": p}
    context.update(get_categories())
    return render(request, 'blog/about.html', context)


def search(request):
    if request.method == 'POST':
        query = request.POST['query']
        posts = Post.objects.filter(content__icontains=query).order_by("-published_date")
    else:
        posts = []
    context = {"posts": posts}
    context.update(get_categories())
    return render(request, "blog/result_search.html", context)


# class CreatePostView(LoginRequiredMixin, CreateView):
#     model = Post
#     template_name = "blog/create.html"
#     login_url = reverse_lazy('login')
#     fields = ('title', 'content', 'category', 'img',)
#     success_url = reverse_lazy('index')
#
#     def post(self, request, *args, **kwargs):
#         form = PostForm(request.POST, files=request.FILES)
#         author = User.objects.get(user=request.user)
#         form.instance.user = author
#         if form.is_valid():
#             form.save()
#             return redirect("index")
#         else:
#             context = {'form': form}
#             return render(request, self.template_name, context)


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "blog/create.html"
    login_url = reverse_lazy('login')
    fields = ('title', 'content', 'category', 'img',)
    success_url = reverse_lazy('index')

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                p = form.save(commit=False)
                p.published_date = now()
                p.user = request.user
                p.save()
                return redirect("index")
            else:
                return render(request, "blog/create.html", {"form": form})
        form = PostForm()
        context = {"form": form}
        context.update(get_categories())
        return render(request, "blog/create.html", context)


# @login_required
# def create(request):
#     # if request.method == 'POST':
#     #     form = PostForm(request.POST, request.FILES)
#     #     if form.is_valid():
#     #         p = form.save(commit=False)
#     #         p.published_date = now()
#     #         p.user = request.user
#     #         p.save()
#     #         return redirect("index")
#     #     else:
#     #         return render(request, "blog/create.html", {"form": form})
#     form = PostForm()
#     context = {"form": form}
#     context.update(get_categories())
#     return render(request, "blog/create.html", context)


@login_required
@require_POST
def like(request, id):
    if request.method == 'POST':
        user = request.user
        post = get_object_or_404(Post, pk=id)
        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
            message = 'Забрати свій лайк з новини'
        else:
            post.likes.add(user)
            message = 'Вам сподобалась ця новина'
    context = {'likes_count': post.total_likes(), 'message': message}
    return JsonResponse(context)


class UpdatePostView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Post
    template_name = "blog/update.html"
    login_url = reverse_lazy('login')
    extra_context = {'title': 'Редагувати пост'}
    fields = ('title', 'content', 'category', 'img',)
    success_url = reverse_lazy('index')

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False


class DeletePostView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Post
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('index')

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False


class PostComment(LoginRequiredMixin, CreateView):
    form = CommentForm
    model = Comment
    login_url = reverse_lazy('login')
    template_name = "blog/post_comment.html"
    extra_context = {'title': 'Коментар до новини'}
    fields = {'text', }
    success_url = reverse_lazy('index')

    def post(self, request, id, *args, **kwargs):
        comment = Comment(text=request.POST.get('text'))
        post = Post.objects.get(pk=id)
        comment.post = post
        comment.user = request.user
        comment.save()
        return redirect("index")


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ('text',)
    template_name = 'blog/update_post_comment.html'
    success_url = reverse_lazy('index')
    extra_context = {'title': 'Редагування коментаря'}
    login_url = reverse_lazy('login')

    def test_func(self):
        comment_id = self.kwargs['pk']
        user = self.request.user
        comment = Comment.objects.get(pk=comment_id)
        if comment.user == user:
            return True
        elif self.request.user.is_staff or self.request.user.is_superuser:
            return True
        return False


class DeleteCommentView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    success_url = reverse_lazy('index')
    extra_context = {'title': 'Видалення коментаря'}
    login_url = reverse_lazy('login')

    def test_func(self):
        comment_id = self.kwargs['pk']
        user = self.request.user
        comment = Comment.objects.get(id=comment_id)
        if comment.user == user:
            return True
        elif self.request.user.is_staff or self.request.user.is_superuser:
            return True
        return False
