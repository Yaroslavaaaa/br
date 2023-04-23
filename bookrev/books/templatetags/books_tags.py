from django import template
from books.models import *

register = template.Library()


@register.simple_tag()
def get_genres():
    return Genres.objects.all()


@register.inclusion_tag('books/list_genres.html')
def show_genres():
    genres = Genres.objects.all()
    return {"genres": genres}