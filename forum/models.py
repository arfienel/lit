from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.conf import settings
from random import randint
from ckeditor.fields import RichTextField


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nickname = models.CharField(max_length=50, default='')
    profile_picture = models.ImageField('profile_picture', upload_to='profile_photos/%y/%m/%d/',
                                        default='filler_images/filler.jpg')
    mod_date = models.DateTimeField('Last modified', auto_now=True)
    likes = models.ManyToManyField(User, related_name='profile_likes', blank=True)

    def number_of_likes(self):
        return self.likes.count()

    class Meta:
        verbose_name = 'User Profile'

    def __str__(self):
        return "{}'s profile".format(self.user.__str__())


# добавить смайлики к тексту, видео, лайки дизлайки
class News(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField('Заголовок', max_length=200)
    text = RichTextField(blank=True, null=True)
    pub_date = models.DateTimeField('дата публикации', auto_now_add=True)
    image = models.ImageField('изображение', upload_to='photos/%y/%m/%d/')
    likes = models.ManyToManyField(User, related_name='news_likes', blank=True)

    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

# добавить лайки и дизлайки


class NewsComments(models.Model):
    com_news = models.ForeignKey(News, on_delete=models.CASCADE)
    com_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    com_text = models.CharField('Комментарий', max_length=300)
    com_date = models.DateTimeField('дата комментария', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий новости'
        verbose_name_plural = 'Коментарии новости'


class Discussions(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tags = TaggableManager()
    title = models.CharField('заголовок', max_length=200)
    text = models.TextField('текст')
    pub_date = models.DateTimeField('дата публикации', auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='discussion_likes', blank=True)

    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Дискусия'
        verbose_name_plural = 'Дискусии'


class DiscussionsComments(models.Model):
    com_discuss = models.ForeignKey(Discussions, on_delete=models.CASCADE)
    com_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    com_text = models.CharField('комментарий', max_length=300)
    com_date = models.DateTimeField('дата комментария', auto_now_add=True)

    class Meta:
        verbose_name = 'Коментарий дискусии'
        verbose_name_plural = 'Коментарии дискускии'


'''
Цикл ( т.е. находится  в общей вселенной книга с другими книгами или чё)
Автор
Название
Отрывок книги ( будет как в бесплатных так и в платных книгах)
Награды книги
Аннотация
Дата публикации
Добавить в понравившиеся ( т.е. пользователь может добавить к себе книгу типо ему понравилось в свой профиль под тегом " Понравилось"
Удобство чтения по главам ( т.е. можно спокойно выбрать главу и читать с неё"
скольким пользователям понравилась и сколько посмотрели 

обсуждения к этой книге - можно сделать путем поиска по тегам и названиям и выводить, а при нажатии перекидывать
на страницу с поиском и результатми

user контактные данные, отметка когда был в сети, соавторство, у статьи можно закрыть комментарии, сверху интерактивное меню по книгам
'''


class Book(models.Model):
    post_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField('обложка книги', upload_to='photos/%y/%m/%d/', default='filler_images/filler.jpg')
    title = models.CharField('название', max_length=200, unique=True)
    #text_example = RichTextField(blank=True, null=True)
    age18 = models.BooleanField('есть контент для взрослых?', default=False)
    ended = models.BooleanField('это произведение окончено?', default=False)
    price = models.PositiveIntegerField('цена')
    start_date = models.DateTimeField('дата начала написания книги', auto_now_add=True)
    tags = TaggableManager()
    likes = models.ManyToManyField(User, related_name='book_likes', blank=True)
    # genre

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'


class BookChapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    title = models.CharField('Название', max_length=100, default='')
    image = models.ImageField('изображение', upload_to='photos/%y/%m/%d/')
    text = RichTextField(blank=True, null=True)
    posted = models.BooleanField('выпущено', default=False)


class BookComments(models.Model):
    com_book = models.ForeignKey(Book, on_delete=models.CASCADE)
    com_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    com_text = models.CharField('Комментарий', max_length=300)
    com_date = models.DateTimeField('дата комментария', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий книги'
        verbose_name_plural = 'Коментарии книги'


class PageHit(models.Model):
    url = models.CharField(unique=True, max_length=2000)
    count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'счётчик'
        verbose_name_plural = 'счётчики'

    def __str__(self):
        return self.url
# Create your models here.
