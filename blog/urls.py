from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, {"pageno": 1}, name='blog-home'),
    path('<int:pageno>', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('post/create/', views.post_create, name='blog-create'),
    path('post/<data>/', views.detailed_content, name='blog-detail'),  # date = title of blog
    path('post/<data>/update/', views.update_post, name='blog-update'),
    path('post/<data>/delete/', views.delete_post, name='blog-delete')
]
