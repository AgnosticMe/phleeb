from django.urls import path
from . import views
from django.contrib.auth import views as authViews

app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'  ),
    path('login/', views.UserLoginView.as_view(), name='login'  ),
    path('logout/', views.UserLogoutView.as_view(), name='logout'  ),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('change-password-done/', views.change_password_done , name='change_password_done'),
    path('update-profile/<slug:slug>/', views.UserProfileUpdateView.as_view(), name='update_profile'  ),
    path('my-profile/', views.UserProfileView.as_view(), name='my_profile'  ),
    path('<int:pk>/', views.UserBlogView.as_view(), name='user_blogs'  ),
    path('', views.UserListView.as_view(), name='users_list'  ),




]
