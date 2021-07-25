from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
admin.site.register(News)
admin.site.register(NewsComments)
admin.site.register(Book)
admin.site.register(BookComments)
admin.site.register(Discussions)
admin.site.register(DiscussionsComments)
# Register your models here.
