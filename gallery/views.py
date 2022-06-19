from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from rest_framework.reverse import reverse_lazy

from .models import Photo
from .forms import PhotoForm
from blog.views import get_categories
from django.shortcuts import render, redirect


def gallery(request):
    photos = Photo.objects.all()
    context = {"photos": photos}
    context.update(get_categories())
    return render(request, "gallery/index.html", context)


class CreatePhotoView(LoginRequiredMixin, CreateView):
    model = Photo
    template_name = "gallery/upload.html"
    login_url = reverse_lazy('login')
    fields = ('image', 'description',)
    success_url = reverse_lazy('gallery')

def post(self, request, *args, **kwargs):
    form = PhotoForm(request.POST, files=request.FILES)
    author = User.objects.get(user=request.user)
    form.instance.user = author
    if form.is_valid():
        form.save()
        return redirect("gallery")
    else:
        context = {'form': form}
        context.update(get_categories())
        return render(request, self.template_name, context)

# @login_required
# def upload(request):
#     if request.method == "POST":
#         form = PhotoForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect("gallery")
#     form = PhotoForm()
#     context = {"form": form}
#     context.update(get_categories())
#     return render(request, "gallery/upload.html", context)
