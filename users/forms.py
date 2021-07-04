from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import fields
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from .models import UserProfile


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=50)
    password1 = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')



class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_class = 'mt-10'
        self.helper.layout = Layout(
            Field('date_of_birth', css_class= 'single-input'),
            Field('bio', css_class= 'single-input'),
            Field('image', css_class= 'single-input'),

        )

        self.helper.add_input(Submit('Submit', 'Update', css_class= 'genric-btn success-border medium'))

    class Meta:
        model = UserProfile
        fields = ('date_of_birth', 'bio', 'image')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type':'date'})
        }



