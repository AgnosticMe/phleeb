from django.contrib import admin
from .models import Blog, Category, Tag, Comment

# Register your models here.
@admin.register(Blog)
class AdminBlog(admin.ModelAdmin):
    list_display = ['title', 'publishing_date']
    list_display_links = ['title', 'publishing_date']
    list_filter = ['publishing_date', 'category', 'tag']
    search_fields = ['title', 'content']

    class Meta:
        model = Blog

@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']

    class Meta:
        model = Category


@admin.register(Tag)
class AdminTag(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']

    class Meta:
        model = Tag


@admin.register(Comment)
class AdminComment(admin.ModelAdmin):
    search_fields = ['name', 'email', 'content', 'blog__title']
    list_filter = ['publishing_date']

    class Meta:
        model = Comment

