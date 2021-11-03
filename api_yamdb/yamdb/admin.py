from django.contrib import admin
from .models import User, Genre, Titles, Genre_title

admin.site.register(User)
admin.site.register(Genre_title)
admin.site.register(Titles)
admin.site.register(Genre)
