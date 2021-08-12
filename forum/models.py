from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.conf import settings
from random import randint
from ckeditor.fields import RichTextField
from django_resized import ResizedImageField
from django.shortcuts import get_object_or_404


# TODO библиотека пользователя

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nickname = models.CharField(max_length=50, default='')
    profile_picture = ResizedImageField('profile_picture', upload_to='profile_photos/%y/%m/%d/',
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
    views = models.PositiveBigIntegerField(default=0)
    pub_date = models.DateTimeField('дата публикации', auto_now_add=True)
    image = ResizedImageField('изображение', upload_to='photos/%y/%m/%d/')
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
    annotate = RichTextField(default='')
    views = models.PositiveBigIntegerField(default=0)
    age18 = models.BooleanField('есть контент для взрослых?', default=False)
    ended = models.BooleanField('это произведение окончено?', default=False)
    price = models.PositiveIntegerField('цена')
    pub_date = models.DateField('дата обновления книги', auto_now=True)
    tags = TaggableManager()
    likes = models.ManyToManyField(User, related_name='book_likes', blank=True)

    genre_choices = [
        ('detective', 'Детектив'),
        ('his_detective', 'Исторический детектив'),
        ('fantastic_detective', 'Фантастический детектив'),
        ('spy_detective', 'Шпионский детектив'),
        ('his_prose', 'Историческая проза'),
        ('litRPG', 'ЛитРПГ'),
        ('realRPG', 'РеалРПГ'),
        ('love_roman', 'Любовные романы'),
        ('his_love_roman', 'Исторический любовный роман'),
        ('short_love_roman', 'Короткий любовный роман'),
        ('love_fantastic', 'Любовная фантастика'),
        ('love_fantasy', 'Любовное фэнтези'),
        ('modern_love_roman', 'Современный любовный роман'),
        ('mystic', 'Мистика'),
        ('teen_prose', 'Подростковая проза'),
        ('political_roman', 'Политический роман'),
        ('fallout', 'Попаданцы'),
        ('fallout_in_space', 'Попаданцы в космос'),
        ('fallout_in_magical_world', 'Попаданцы в магические миры'),
        ('fallout_in_time', 'Попаданцы во времени'),
        ('poetry', 'Поэзия'),
        ('adventure', 'Приключения'),
        ('different', 'Разное'),
        ('business_literature', 'Бизнес - литература'),
        ('kid_literature', 'Детская литература'),
        ('documentary_prose', 'Документальная проза'),
        ('public', 'Публицистика'),
        ('personal development', 'Развитие личности'),
        ('fairy_tale', 'Сказка'),
        ('modern_prose', 'Современная проза'),
        ('thriller', 'Триллер'),
        ('horror', 'Ужасы'),
        ('fantastic', 'Фантастика'),
        ('alternative_history', 'Альтернативная история'),
        ('anti_utopia', 'Антиутопия'),
        ('battle_fantastic', 'Боевая фантастика'),
        ('heroes_fantastic', 'Героическая фантастика'),
        ('cyberpunk', 'Киберпанк'),
        ('cosmical_fantastic', 'Космическая фантастика'),
        ('science_fantastic', 'Научная фантастика'),
        ('post_apocalypse', 'Постапокалипсис'),
        ('social_fantastic', 'Социальная фантастика'),
        ('steampunk', 'Стимпанк'),
        ('humor_fantastic', 'Юмористическая фантастика'),
        ('fanfic', 'Фанфик'),
        ('fantasy', 'Фэнтези'),
        ('battle_fantasy', 'Боевое фэнтези'),
        ('heroes_fantasy', 'Героическое фэнтези'),
        ('town_fantasy', 'Городское фэнтези'),
        ('historical_fantasy', 'Историческое фэнтези'),
        ('dark_fantasy', 'Темное фэнтези'),
        ('epic_fantasy', 'Эпическое фэнтези'),
        ('humor_fantasy', 'Юмористическое фэнтези'),
        ('erotic', 'Эротика'),
        ('novel_erotic', 'Романтическая эротика'),
        ('slash', 'Слэш'),
        ('fem_slash', 'Фэмслеш'),
        ('erotic_fantastic', 'Эротическая фантастика'),
        ('erotic_fanfic', 'Эротический фанфик'),
        ('erotic_fantasy', 'Эротическое фэнтези'),
        ('humor', 'Юмор'),
    ]

    main_genre = models.CharField(max_length=70, choices=genre_choices)
    add_genre_1 = models.CharField(max_length=70, choices=genre_choices)
    add_genre_2 = models.CharField(max_length=70, choices=genre_choices)

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
