from django.contrib import admin

from .models import Comment, Genre, Genre_title, Review, Title

admin.site.register(Genre_title)
admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(Comment)
admin.site.register(Review)
