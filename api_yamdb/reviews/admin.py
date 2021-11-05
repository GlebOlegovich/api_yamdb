from django.contrib import admin
from .models import User, Genre, Title, Genre_title, Comment, Review

admin.site.register(User)
admin.site.register(Genre_title)
admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(Review)
admin.site.register(Comment)
