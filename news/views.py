from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.core.cache import cache
import logging

from .models import *
from .filters import NewsFilter
from .forms import CreateNewsForm

logger = logging.getLogger(__name__)

class NewsList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'mainnews.html'
    context_object_name = 'posts'
    paginate_by = 10


    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class Textnews(DetailView):
    model = Post
    template_name = 'textnews.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj

class CreateNews(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    form_class = CreateNewsForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.categoryType= 'NW'
        return super().form_valid(form)


class UpdateNews(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    form_class = CreateNewsForm
    model = Post
    template_name = 'news_edit.html'


class DeleteNews(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    model = Post
    template_name = 'news_delete.html'
    success_url= reverse_lazy('News_list')

class ArticlesCreate(PermissionRequiredMixin,CreateView):
    permission_required = ('news.add_post')
    form_class = CreateNewsForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.categoryType= 'AR'
        return super().form_valid(form)


class UpdateArticles(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    form_class = CreateNewsForm
    model = Post
    template_name = 'news_edit.html'


class DeleteArticles(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('News_list')


class CategoryListView(ListView):
    model = Post
    template_name = 'categorylist.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(postCategory=self.category).order_by('-dateCreation')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['is_subscriber'] = self.request.user in self.category.subscribers.all()
        context['category'] = self.category
        return context

@login_required
@csrf_protect
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно оформили подписку'
    return render(request, 'subscribe.html', {'category': category, 'message': message})

@login_required
@csrf_protect
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)

    message = 'Вы успешно отписались'
    return  render(request, 'unsubscribe.html', {'category': category, 'message': message})