from django.contrib import admin
from .models import User, Genre, Titles, Genre_title, Comment, Review

admin.site.register(User)
admin.site.register(Genre_title)
admin.site.register(Titles)
admin.site.register(Genre)
admin.site.register(Comment)
admin.site.register(Review)
