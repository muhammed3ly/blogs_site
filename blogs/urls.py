from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('posts', views.AllPosts.as_view(), name='posts'),
    path('posts/<slug:slug>', views.PostDetail.as_view(), name='post-detail'),
    path('read-later', views.ReadLaterView.as_view(), name='read-later'),
]
