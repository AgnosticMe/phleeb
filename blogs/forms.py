from crispy_forms.layout import Layout
from django import forms
from django.db.models import fields
from .models import Blog, Comment 
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from captcha.fields import ReCaptchaField


class PostCreationForm(forms.ModelForm):

    class Meta:
        model = Blog
        widgets = {
            'title': forms.TextInput(attrs={'class': 'single-input', 'placeholder':'Enter Blog title'}),
            'content': forms.Textarea(attrs={'class': 'single-input', 'placeholder':'Enter Blog Content'}),

        }

        fields = [ 'title', 'category', 'content', 'image' ]



class BlogUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BlogUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper._form_method = 'POST'
        self.helper.field_class = 'mt-10'
        self.helper.layout = Layout(
            Field('title', css_class='single-input', placeholder="Title"),
            Field('category', css_class='single-input'),
            Field('content', css_class='single-input', placeholder="Your Content"),
            Field('image', css_class='single-input'),
            Field('tag', css_class='single-input', placeholder="Tags", value=self.instance.blog_tags()),
        )

        self.helper.add_input(Submit('submit', 'Update', css_class='generic-btn success circle'))

    tag = forms.CharField()
    class Meta:
        model = Blog
        fields = ['title', 'category', 'content', 'image']




class CreateCommentForm(forms.ModelForm):
    captcha = ReCaptchaField()
    
    def __init__(self, *args, **kwargs):
        super(CreateCommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Field('name', css_class='form-control', placeholder="Enter your Name"),
            Field('email', css_class='form-control', placeholder="Enter your Email"),
            Field('content', css_class='form-control mb-10', placeholder="Write your Comment"),
            Field('captcha'),
        )

        self.helper.add_input(Submit('submit', 'Comment', css_class='primary-btn submit-btn'))

    class Meta:
        model = Comment
        fields = ['name', 'email', 'content']