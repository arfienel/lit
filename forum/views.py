from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponseRedirect
from .models import *
from .forms import *
from itertools import chain
from django.contrib.auth.decorators import login_required
from .services import *
from datetime import datetime


@login_required
def profile(request, pk):
    user = get_object_or_404(UserProfile, user=get_object_or_404(User, pk=pk))
    likes_func(user, request, 'forum:book_detail')
    post_is_liked = user.likes.filter(id=request.user.id).exists()
    return render(request, 'account/profile.html', {'user_profile': user, 'post_is_liked': post_is_liked})


@login_required
def profile_update(request):
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)

    if request.method == "POST":
        form = ProfileForm(request.POST)

        if form.is_valid():
            user_profile.profile_picture = request.FILES['profile_picture']
            user_profile.nickname = form.cleaned_data['nickname']
            user_profile.save()
            return HttpResponseRedirect(reverse('forum:profile', args=[user.pk]))
    else:
        default_data = {'profile_picture': user_profile.profile_picture}
        form = ProfileForm(default_data)

    return render(request, 'account/profile_update.html', {'form': form, 'user': user})


def add_news(request):
    if request.method == "POST":
        form = NewsForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.image = request.FILES['image']
            post.save()
    else:
        form = NewsForm()
    return render(request, 'news/add_news.html', {'form': form})


def add_discussion(request):
    if request.method == "POST":
        form = DiscussionForm(request.POST)
        print(form.errors)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
    else:
        form = DiscussionForm()
    return render(request, 'discussion/add_discussion.html', {'form': form})


def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            post = form.save(commit=False)
            post.post_author = request.user
            post.image = request.FILES['image']
            post.save()
    else:
        form = BookForm()
    return render(request, 'book/add_book.html', {'form': form})


def news_search(request):
    quest = request.GET.get('search')
    title_result = News.objects.filter(title__icontains=quest)
    date_result = News.objects.filter(pub_date__icontains=quest)
    result_list = list(set(chain(title_result, date_result)))

    return render(request, 'news/search-results.html', {'result': result_list})


def book_search(request):
    quest = request.GET.get('search')
    title_result = Book.objects.filter(title__icontains=quest)
    author_result = Book.objects.filter(book_author__icontains=quest)
    tag_search = Book.objects.filter(tags__name__icontains=quest)
    result_list = list(set(chain(title_result, author_result, tag_search)))

    return render(request, 'book/search-results.html', {'result': result_list})


def discussion_search(request):
    quest = request.GET.get('search')
    result = Discussions.objects.filter(title__icontains=quest)
    return render(request, 'discussion/search-results.html', {'result': result})


def main_page(request):
    return render(request, 'main.html', {})


def book_list(request):
    books = Book.objects.order_by('likes')
    return render(request, 'book/book_list.html', {'books': books})


def book_detail(request, pk):
    book = Book.objects.get(pk=pk)
    comment_func(BookComments, book, request)
    comments = BookComments.objects.filter(com_book=book)
    likes_func(book, request, 'forum:book_detail')
    post_is_liked = book.likes.filter(id=request.user.id).exists()
    return render(request, 'book/book_detail.html', {'book': book, 'comments': comments,
                                                     'post_is_liked': post_is_liked})


def discussion_list(request):
    discussions = Discussions.objects.order_by('likes')
    return render(request, 'discussion/discussion_list.html', {'discussions': discussions})


def discussion_detail(request, pk):
    discussion = Discussions.objects.get(pk=pk)

    comment_func(DiscussionsComments, discussion, request)
    comments = DiscussionsComments.objects.filter(com_discuss=discussion)

    likes_func(discussion, request, 'forum:discussion_detail')
    post_is_liked = discussion.likes.filter(id=request.user.id).exists()

    return render(request, 'discussion/discussion_detail.html', {'discussion': discussion,
                                                                 'comments': comments, 'post_is_liked': post_is_liked})


def news_list(request):
    news = News.objects.order_by('likes')
    return render(request, 'news/news_list.html', {'news': news})


def news_detail(request, pk):
    news = News.objects.get(pk=pk)
    comment_func(NewsComments, news, request)
    comments = NewsComments.objects.filter(com_news=news)

    # лайки их удаление и добавление
    likes_func(news, request, 'forum:news_detail')
    post_is_liked = news.likes.filter(id=request.user.id).exists()

    return render(request, 'news/news_detail.html', {'news': news, 'comments': comments,
                                                     'post_is_liked': post_is_liked})

# Create your views here.
