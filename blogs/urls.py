from django.urls import path
from . import views

app_name = 'blogs'

urlpatterns = [
    path('',  views.IndexView.as_view(), name='index'),
    path('detail/<int:pk>/<slug:slug>', views.BlogDetail.as_view(), name='detail'),
    path('category/<int:pk>/<slug:slug>', views.CategoryDetail.as_view(), name='category_detail'),
    path('tag/<int:pk>/<slug:slug>', views.TagDetail.as_view(), name='tag_detail'),
    path('create-blog/', views.CreateBlogView.as_view(), name='create_blog'),
    path('update-blog/<int:pk>/<slug:slug>', views.BlogUpdateView.as_view(), name='update_blog'),
    path('delete-blog/<int:pk>/<slug:slug>', views.DeleteBlogView.as_view(), name='delete_blog'),
    path('search/', views.SearchView.as_view(), name='search')



]

