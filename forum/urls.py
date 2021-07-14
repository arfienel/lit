from django.urls import path
from .views import *


app_name = 'forum'
urlpatterns = [
    path('', main_page, name='main_page')
]
