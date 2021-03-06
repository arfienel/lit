from django.shortcuts import redirect, reverse, get_object_or_404
from django.http import Http404
from .models import *


# функция лайков, подставлям сюда модель, request и url куда должно перекидывать потом
def likes_func(model, request, redirection: str):
    if request.method == "POST" and "like" in request.POST:
        if model.likes.filter(id=request.user.id).exists():
            model.likes.remove(request.user)
            return redirect(reverse(redirection, args=[model.pk]))
        else:
            model.likes.add(request.user)
            return redirect(reverse(redirection, args=[model.pk]))


# комментарии и их добавление
def comment_func(com_model, post_model, request):
    tip = com_model.__doc__
    tip = tip[tip.find('('):].split(', ')[1]
    tip = tip.replace('com_', '')
    if request.method == "POST" and 'comment' in request.POST:
        if tip == 'book':
            new_comment = com_model(com_book=post_model, com_author=request.user,
                                    com_text=request.POST['comment'])
        elif tip == 'discuss':
            new_comment = com_model(com_discuss=post_model, com_author=request.user,
                                    com_text=request.POST['comment'])
        elif tip == 'news':
            new_comment = com_model(com_news=post_model, com_author=request.user,
                                    com_text=request.POST['comment'])
        else:
            raise NameError('something went wrong in comment_func')
        new_comment.save()
        return redirect(reverse(f'forum:{tip}_detail', args=[post_model.pk]))


def views_add(request):
    options = request.path.split('/')
    try:
        options.remove(''), options.remove('')
    except ValueError:
        return None
    if len(options) == 2 and type(options[1]) == int:
        if options[0] == 'books':
            obj = Book.objects.get(pk=options[1])
            obj.views += 1
            obj.save()
        if options[0] == 'news':
            obj = News.objects.get(pk=options[1])
            obj.views += 1
            obj.save += 1


# функция чтобы узнать пользователь владелец или нет
def is_owner(request, pk):
    if request.user.pk == pk:
        return True
    else:
        return False


def user_prof_find(pk):
    try:
        return get_object_or_404(UserProfile, pk=pk)
    except Http404:
        return None
