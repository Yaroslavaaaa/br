from django.contrib import admin
from django.utils.safestring import mark_safe

# Register your models here.

from .models import *

class BooksAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'genre', 'get_html_photo', 'is_published', 'user')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    prepopulated_fields = {"slug": ("title",)}
    fields = ('title', 'slug', 'genre', 'description', 'author', 'image', 'is_published', 'pub_date', 'get_html_photo')
    readonly_fields = ('get_html_photo', )
    save_on_top = True

    def get_html_photo(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}' width=50>")

    get_html_photo.short_description = "Миниатюра"


class GenresAdmin(admin.ModelAdmin):
    list_display = ('id', 'genre_name')
    list_display_links = ('id', 'genre_name')
    search_fields = ('genre_name',)
    prepopulated_fields = {"slug": ("genre_name",)}



class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'com_text')
    list_display_links = ('id', 'com_text')
    search_fields = ('com_text',)
    # prepopulated_fields = {"slug": ("genre_name",)}

class AnsCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'ans_com_text')
    list_display_links = ('id', 'ans_com_text')
    search_fields = ('ans_com_text',)

class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'role_name')
    list_display_links = ('id', 'role_name')
    search_fields = ('role_name',)



class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')
    list_display_links = ('id', 'username')
    search_fields = ('username',)

    def get_html_avatar(self, object):
        if object.avatar:
            return mark_safe(f"<img src='{object.avatar.url}' width=50>")

    get_html_avatar.short_description = "Миниатюра"


# class EmployeeInline(admin.StackedInline):
#     model = CustomUser
#     can_delete = False
#     verbose_name_plural = 'employee'




admin.site.register(Books, BooksAdmin)
admin.site.register(Genres, GenresAdmin)
admin.site.register(Comments, CommentAdmin)
admin.site.register(Roles, RoleAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CommentsAns, AnsCommentAdmin)

admin.site.site_title = 'Админ-панель книжного сайта'
admin.site.site_header = 'Админ-панель книжного сайта'



