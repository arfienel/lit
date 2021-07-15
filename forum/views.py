from django.shortcuts import render
from .models import *


def main_page(request):
    return render(request, 'main.html', {})


def book_list(request):
    books = Book.objects.order_by('likes')
    return render(request, 'book/book_list.html', {'books': books})


def book_detail(request, pk):
    book = Book.objects.get(pk=pk)
    return render(request, 'book/book_detail.html', {'book': book})


def discussion_list(request):
    discussions = Discussions.objects.order_by('likes')
    return render(request, 'discussion/discussion_list.html', {'discussions': discussions})


def discussion_detail(request, pk):
    discussion = Discussions.objects.get(pk=pk)
    if request.method == "POST" and 'comment' in request.POST:
        print(request.POST)
        new_comment = DiscussionsComments(com_discuss=discussion, com_author=request.user,
                                          com_text=request.POST['comment'])
        new_comment.save()
    elif request.method == "POST" and 'like' in request.POST:
        print('like')
        print(request.POST)
    comments = DiscussionsComments.objects.filter(com_discuss=discussion)
    print(comments)
    return render(request, 'discussion/discussion_detail.html', {'discussion': discussion, })


def news_list(request):
    news = News.objects.order_by('likes')
    return render(request, 'news/news_list.html', {'news': news})


def news_detail(request, pk):
    news = News.objects.get(pk=pk)
    return render(request, 'news/news_detail.html', {'news': news})

# Create your views here.
