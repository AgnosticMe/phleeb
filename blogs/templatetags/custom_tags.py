from django import template
from blogs.models import Blog, Category, Tag

register = template.Library()

@register.simple_tag(name="categories")
def all_categories():
    return Category.objects.all()


@register.simple_tag(name="tags")
def all_tags():
    return Tag.objects.all


@register.simple_tag(name="blogs_hit")
def blogs_hit():
    return Blog.objects.order_by('-hit')[:5]