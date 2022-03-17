from django.urls import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from datetime import date
from .models import Post
from .forms import CommentForm
from django.views.generic import ListView
from django.views import View


class Index(ListView):
    template_name = 'blogs/index.html'
    model = Post
    context_object_name = 'posts'
    ordering = ['-date']

    def get_queryset(self):
        query_set = super().get_queryset()
        return query_set[:3]


class AllPosts(ListView):
    template_name = 'blogs/all-posts.html'
    model = Post
    context_object_name = 'posts'
    ordering = ['-date']


class PostDetail(View):
    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        context = {
            'post': post,
            'tags': post.tags.all(),
            'form': CommentForm(),
            'comments': post.comments.all().order_by('-id')
        }
        return render(request, 'blogs/post-detail.html', context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('post-detail', args=[slug]))

        context = {
            'post': post,
            'tags': post.tags.all(),
            'form': comment_form,
            'comments': post.comments.all().order_by('-id')
        }
        return render(request, 'blogs/post-detail.html', context)


class ReadLaterView(View):
    def get(self, request):
        read_later_posts = request.session.get('read_later_posts')

        context = {}

        if read_later_posts is None or len(read_later_posts) == 0:
            context['posts'] = []
            context['has_posts'] = False
        else:
            context['posts'] = Post.objects.filter(id__in=read_later_posts)
            context['has_posts'] = True

        return render(request, 'blogs/read-later-posts.html', context)

    def post(self, request):
        read_later_posts = request.session.get('read_later_posts')
        if read_later_posts is None:
            read_later_posts = []

        post_id = int(request.POST['post_id'])
        if post_id not in read_later_posts:
            read_later_posts.append(post_id)
            request.session['read_later_posts'] = read_later_posts

        return HttpResponseRedirect('/read-later')
