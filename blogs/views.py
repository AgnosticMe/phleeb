from django.shortcuts import get_object_or_404, render
from django.utils.text import slugify
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Blog, Category, Tag
from .forms import CreateCommentForm, PostCreationForm, BlogUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import F, Q
from django.views.generic.edit import FormMixin

# Create your views here.


class IndexView(ListView):
    template_name = 'blogs/index.html'
    model = Blog
    context_object_name = 'blogs'
    paginate_by = 3

    def get_context_data(self,  **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['slider_posts'] = Blog.objects.all().filter(slider_blog=True)
        return context


class BlogDetail(DetailView, FormMixin):
    template_name = 'blogs/detail.html'
    model = Blog
    context_object_name = 'blog_detail'
    form_class = CreateCommentForm

    def get(self, request, *args, **kwargs):
        self.hit = Blog.objects.filter(
            id=self.kwargs['pk']).update(hit=F('hit')+1)
        return super(BlogDetail, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BlogDetail, self).get_context_data(**kwargs)
        context['previous'] = Blog.objects.filter(
            id__lt=self.kwargs['pk']).order_by('-id').first()
        context['next'] = Blog.objects.filter(
            id__gt=self.kwargs['pk']).order_by('id').first()
        context['form'] = self.get_form()
        return context

    def form_valid(self, form):
        if form.is_valid():
            form.instance.blog = self.object
            form.save()
            return super(BlogDetail, self).form_valid(form)
        else:
            return super(BlogDetail, self).form_invalid(form)

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_valid(form)

    def get_success_url(self):
        return reverse('blogs:detail', kwargs={'pk':self.object.pk, 'slug':self.object.slug})


class CategoryDetail(ListView):
    model = Blog
    template_name = 'categories/category_detail.html'
    context_object_name = 'category_posts'
    paginate_by = 3

    def get_queryset(self):
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        return Blog.objects.filter(category=self.category).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(CategoryDetail, self).get_context_data(**kwargs)
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        context['category'] = self.category
        return context


class TagDetail(ListView):
    model = Blog
    template_name = 'tags/tag_detail.html'
    context_object_name = 'tag_posts'
    paginate_by = 3

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, pk=self.kwargs['pk'])
        return Blog.objects.filter(tag=self.tag).order_by('id')

    def get_context_data(self, **kwargs):
        context = super(TagDetail, self).get_context_data(**kwargs)
        self.tag = get_object_or_404(Tag, pk=self.kwargs['pk'])
        context['tag'] = self.tag
        return context


class CreateBlogView(LoginRequiredMixin, CreateView):
    template_name = 'blogs/create_blog.html'
    form_class = PostCreationForm
    model = Blog

    def get_success_url(self):
        return reverse('blogs:detail', kwargs={'pk': self.object.pk, 'slug': self.object.slug})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()

        tags = self.request.POST.get('tag').split(',')

        for tag in tags:
            current_tag = Tag.objects.filter(slug=slugify(tag))
            if current_tag.count() < 1:
                create_tag = Tag.objects.create(title=tag)
                form.instance.tag.add(create_tag)
            else:
                existing_tag = Tag.objects.get(slug=slugify(tag))
                form.instance.tag.add(existing_tag)

        return super(CreateBlogView, self).form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'blogs/update_blog.html'
    form_class = BlogUpdateForm
    model = Blog

    def get_success_url(self):
        return reverse('blogs:detail', kwargs={'pk': self.object.pk, 'slug': self.object.slug})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.tag.clear()

        tags = self.request.POST.get('tag').split(',')

        for tag in tags:
            current_tag = Tag.objects.filter(slug=slugify(tag))
            if current_tag.count() < 1:
                create_tag = Tag.objects.create(title=tag)
                form.instance.tag.add(create_tag)
            else:
                existing_tag = Tag.objects.get(slug=slugify(tag))
                form.instance.tag.add(existing_tag)

        return super(BlogUpdateView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.user != request.user:
            return HttpResponseRedirect('/')
        return super(BlogUpdateView, self).get(request, *args, **kwargs)


class DeleteBlogView(DeleteView):
    model = Blog
    template_name = 'blogs/delete_blog.html'
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user == request.user:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        else:
            return HttpResponseRedirect(self.success_url)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != request.user:
            return HttpResponseRedirect('/')

        return super(DeleteBlogView, self).get(request, *args, **kwargs)


class SearchView(ListView):
    model = Blog
    template_name = 'blogs/search.html'
    paginate_by = 3
    context_object_name = 'blogs'

    def get_queryset(self):
        query = self.request.GET.get('q')

        if query:
            return Blog.objects.filter(Q(title__icontains=query) |
                                       Q(content__icontains=query) |
                                       Q(tag__title__icontains=query)).order_by('id').distinct()

        return Blog.objects.all().order_by('id')
