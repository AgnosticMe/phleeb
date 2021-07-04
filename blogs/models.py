from django.db import models
from django.conf import settings
from django.utils.text import slugify
import uuid

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(editable=False)


    def save(self, *args, **kwargs):
        self.slug = f'{slugify(self.title)}--{uuid.uuid4()}'
        super(Category, self).save(*args, **kwargs)


    def __str__(self):
        return self.title

    def blog_count(self):
        return self.blogs.all().count()


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def blog_count(self):
        return self.blogs.all().count()


class Blog(models.Model):   
    title = models.CharField(max_length=150)
    content = models.TextField()
    publishing_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, related_name='blogs')
    tag = models.ManyToManyField(Tag, related_name='blogs', blank=True)
    slider_blog = models.BooleanField(default=False)
    hit = models.PositiveIntegerField(default=0)

    def comment_count(self):
        return self.comments.all().count()

    def save(self, *args, **kwargs):
        self.slug = f'{slugify(self.title)}--{uuid.uuid4()}'
        super(Blog, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def blog_tags(self):
        return ', '.join(str(tag) for tag in self.tag.all())



class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)
    content = models.TextField()
    publishing_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.blog.title



