from django.urls import path
from .views import *
from django.contrib.auth import views

app_name = 'forum'
urlpatterns = [
    path('', main_page, name='main_page'),
    path('books/', book_list, name='book_list'),
    path('books/<int:pk>/', book_detail, name='book_detail'),
    path('books/search/', book_search, name='book_search'),
    path('books/add/', add_book, name='add_book'),
    path('books/read_chapter/<int:pk>', read_chapter, name='read_chapter'),
    path('books/<int:pk>/add_chapter', add_chapter, name='chapter_add'),
    path('books/<int:pk>/edit_book', edit_book, name='edit_book'),
    path('books/<int:pk>/edit_chapter', edit_chapter, name='edit_chapter'),

    path('news/', news_list, name='news_list'),
    path('news/<int:pk>/', news_detail, name='news_detail'),
    path('news/search/', news_search, name='news_search'),
    path('news/add/', add_news, name='add_news'),

    path('discussions/', discussion_list, name='discussion_list'),
    path('discussions/<int:pk>/', discussion_detail, name='discussion_detail'),
    path('discussions/search', discussion_search, name='discussion_search'),
    path('discussions/add', add_discussion, name='add_discussion'),

    path('profile/<int:pk>/', profile, name='profile'),
    path('profile/update/', profile_update, name='profile_update'),
    path('profile/<int:pk>/your_books', profile_books, name='profile_books')
]
