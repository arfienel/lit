from django.shortcuts import render, redirect, reverse
from .models import *


# функция лайков, подставлям сюда модель, request и куда должно перекидывать потом
def likes(model, request, redirection: str):
    if request.method == "POST" and "like" in request.POST:
        if model.likes.filter(id=request.user.id).exists():
            model.likes.remove(request.user)
            return redirect(reverse(redirection, args=[model.pk]))
        else:
            model.likes.add(request.user)
            return redirect(reverse(redirection, args=[model.pk]))


def main_page(request):
    return render(request, 'main.html', {})


def book_list(request):
    books = Book.objects.order_by('likes')
    return render(request, 'book/book_list.html', {'books': books})


def book_detail(request, pk):
    book = Book.objects.get(pk=pk)
    # комментарии и их добавление
    if request.method == "POST" and 'comment' in request.POST:
        new_comment = BookComments(com_book=book, com_author=request.user,
                                   com_text=request.POST['comment'])
        new_comment.save()
        return redirect(reverse('forum:book_detail', args=[book.pk]))
    comments = BookComments.objects.filter(com_book=book)

    # лайки их удаление и добавление
    likes(book, request, 'forum:book_detail')
    post_is_liked = book.likes.filter(id=request.user.id).exists()
    return render(request, 'book/book_detail.html', {'book': book, 'comments': comments,
                                                     'post_is_liked': post_is_liked})


def discussion_list(request):
    discussions = Discussions.objects.order_by('likes')
    return render(request, 'discussion/discussion_list.html', {'discussions': discussions})


def discussion_detail(request, pk):
    discussion = Discussions.objects.get(pk=pk)

    # комментарии и их добавление
    if request.method == "POST" and 'comment' in request.POST:
        new_comment = DiscussionsComments(com_discuss=discussion, com_author=request.user,
                                          com_text=request.POST['comment'])
        new_comment.save()
        return redirect(reverse('forum:discussion_detail', args=[discussion.pk]))

    comments = DiscussionsComments.objects.filter(com_discuss=discussion)

    # лайки их удаление и добавление
    likes(discussion, request, 'forum:discussion_detail')
    post_is_liked = discussion.likes.filter(id=request.user.id).exists()

    return render(request, 'discussion/discussion_detail.html', {'discussion': discussion,
                                                                 'comments': comments, 'post_is_liked': post_is_liked})


def news_list(request):
    news = News.objects.order_by('likes')
    return render(request, 'news/news_list.html', {'news': news})


def news_detail(request, pk):
    news = News.objects.get(pk=pk)

    # комментарии и их добавление
    if request.method == "POST" and 'comment' in request.POST:
        new_comment = NewsComments(com_news=news, com_author=request.user,
                                   com_text=request.POST['comment'])
        new_comment.save()
        return redirect(reverse('forum:news_detail', args=[news.pk]))
    comments = NewsComments.objects.filter(com_news=news)

    # лайки их удаление и добавление
    likes(news, request, 'forum:news_detail')
    post_is_liked = news.likes.filter(id=request.user.id).exists()

    return render(request, 'news/news_detail.html', {'news': news, 'comments': comments,
                                                     'post_is_liked': post_is_liked})

# Create your views here.
