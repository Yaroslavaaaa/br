from django.db.models import Count
from django.core.cache import cache

from .models import *


menu = [{'title': "Главная", 'url_name': "index"},
        {'title': "Добавить книгу", 'url_name': "add"},
        ]

class DataMixin:
    paginate_by = 4
    def get_user_context(self, **kwargs):
        context = kwargs

        # genres = cache.get('genres')
        # if not genres:
        #     genres = Genres.objects.annotate(Count('books'))
        #     cache.set('genres', genres, 60)

        genres = Genres.objects.annotate(Count('books'))





        user_menu = menu.copy()
        if not self.request.user.is_authenticated or not self.request.user.is_superuser:
            user_menu.pop(1)

        context['menu'] = user_menu


        context['genres'] = genres
        if 'genre_selected' not in context:
            context['genre_selected'] = 0

        return context