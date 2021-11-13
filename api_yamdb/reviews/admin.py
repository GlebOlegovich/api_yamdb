from django.contrib import admin
<<<<<<< HEAD
from .models import Genre, Title, Genre_title, Comment, Review

=======

from .models import Comment, Genre, Genre_title, Review, Title

>>>>>>> 5cd77ba2e9878adc1972fc6605528422e73bf096
admin.site.register(Genre_title)
admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(Comment)
admin.site.register(Review)
