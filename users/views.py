from django import template
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse
from .forms import RegisterForm, UserProfileForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic import CreateView, UpdateView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordChangeForm
from .models import UserProfile
from blogs.models import Blog
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.
class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    success_url = '/'
    


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    


class UserLogoutView(LogoutView):
    template_name = 'users/login.html'



class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/password_change_form.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('users:change_password_done')


def change_password_done(request):
    return render(request, 'users/password_change_done.html', {})


class UserProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = UserProfile
    template_name = 'users/profile-update.html'
    form_class = UserProfileForm
    success_message = "Your profile has been updated successfully :)"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super(UserProfileUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('users:update_profile', kwargs={'slug': self.object.slug})

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != request.user:
            return HttpResponseRedirect('/')

        return super(UserProfileUpdateView, self).get(request, *args, **kwargs)


class UserProfileView(LoginRequiredMixin, ListView):
    template_name = 'users/my-profile.html'
    model = Blog
    context_object_name = 'user_posts'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context["userprofile"] = UserProfile.objects.get(user=self.request.user)
        return context

    def get_queryset(self):
        return Blog.objects.filter(user=self.request.user).order_by('-id')


class UserBlogView(ListView):
    template_name = 'users/user-blogs.html'
    model = Blog
    context_object_name = 'blogs'
    paginate_by = 3

    def get_queryset(self,):
        return Blog.objects.filter(user=self.kwargs['pk'])



class UserListView(ListView):
    template_name = 'users/user-list.html'
    model = UserProfile
    context_object_name = 'profiles'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        return context
    
    



    
    

