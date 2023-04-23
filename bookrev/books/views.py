from pyexpat.errors import messages
from urllib import request

from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.http import HttpResponseNotFound, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from rest_framework import generics, viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from rest_framework import generics, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .forms import *
# Create your views here.
from .models import *
from .permissions import *
from .serializers import BooksSerializer
from .utils import *


class BookHome(DataMixin, ListView):
    model = Books
    template_name = 'books/index.html'
    context_object_name = 'books'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        g_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(g_def.items()))

    def get_queryset(self):
        return Books.objects.filter(is_published=True).select_related('genre')



class BookGenre(DataMixin, ListView):
    model = Books
    template_name = 'books/index.html'
    context_object_name = 'books'
    allow_empty = False

    def get_queryset(self):
        return Books.objects.filter(genre__slug=self.kwargs['genre_slug'], is_published=True).select_related('genre')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        g = get_object_or_404(Genres, slug=self.kwargs['genre_slug'])
        g_def = self.get_user_context(title='Категория - ' + str(g.genre_name),
                                      genre_selected=g.pk)
        return dict(list(context.items()) + list(g_def.items()))


class ShowBook(DataMixin, DetailView):
    model = Books
    template_name = 'books/book.html'
    slug_url_kwarg = 'book_slug'
    context_object_name = 'book'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        comments = Comments.objects.filter(book=book.id).prefetch_related('comments_ans', 'comments_ans__user_com_ans')
        context['comments'] = comments
        g_def = self.get_user_context(title=context['book'])
        context['form'] = CommentForm()
        context['form_ans'] = AnsCommentForm()
        comments = book.comments.filter()
        context['comments'] = comments
        g_def = self.get_user_context(title=context['book'])
        context['form'] = CommentForm()

        return dict(list(context.items()) + list(g_def.items()))


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comments
    form_class = CommentForm
    template_name = 'comment_form.html'

    # success_url = reverse_lazy('index')

    def form_valid(self, form):
        book = get_object_or_404(Books, pk=self.kwargs['pk'])
        form.instance.user = self.request.user
        form.instance.book = book
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        book_slug = self.object.book.slug
        success_url = reverse('show_book', kwargs={'book_slug': book_slug})
        return success_url


class AnsCommentCreateView(LoginRequiredMixin, CreateView):
    model = CommentsAns
    form_class = AnsCommentForm
    template_name = 'comment_form.html'

    # success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user_com_ans_id = self.request.user.id
        form.instance.comments_id = self.kwargs['com_pk']
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        book = get_object_or_404(Books, pk=self.kwargs['pk'])
        book_slug = book.slug
        success_url = reverse('show_book', kwargs={'book_slug': book_slug})
        return success_url



class AddBook(DataMixin, CreateView):
    form_class = AddBookForm
    template_name = 'books/add.html'
    success_url = reverse_lazy('index')
    login_url = reverse_lazy('index')
    raise_exception = True

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        return response

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        g_def = self.get_user_context(title="Добавление книги")
        return dict(list(context.items()) + list(g_def.items()))


class Register(DataMixin, CreateView):
    form_class = RegisterForm
    template_name = 'books/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        g_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(g_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')


class Login(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'books/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('index')


class SearchResultsView(DataMixin, ListView):
    model = Books
    template_name = 'books/index.html'
    context_object_name = 'books'

    def get_queryset(self):  # новый
        query = self.request.GET.get('q')
        books = Books.objects.filter(
            Q(title__icontains=query) | Q(title__icontains=query)
        )
        return books

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        g_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(g_def.items()))


class CreateComment(DataMixin, CreateView):
    model = Comments
    form_class = CommentForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        # form.instance.book_id = self.kwargs.get('slug')
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.book.get_absolute_url()
class CreateComment(DataMixin, CreateView):
    model = Comments
    form_class = CommentForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        # form.instance.book_id = self.kwargs.get('slug')
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.book.get_absolute_url()


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        g_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(g_def.items()))


class UserProfile(DataMixin, DetailView):
    model = CustomUser
    template_name = "books/profile.html"
    username_url_kwarg = 'user_username'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return CustomUser.objects.get(username=self.kwargs['user_username'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['user'] = user
        g_def = self.get_user_context(title=context['user'])

        return dict(list(context.items()) + list(g_def.items()))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        g_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(g_def.items()))


class EditUserProfile(DataMixin, UpdateView):
    model = CustomUser
    template_name = "books/edit_profile.html"
    fields = ['first_name', 'last_name', 'username', 'age', 'email', 'avatar']

    def get_success_url(self):
        username = self.request.user.username
        return reverse_lazy('profile', kwargs={'user_username': username})

    def get_object(self):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['first_name'].widget.attrs.update({'class': 'form-input'})
        form.fields['last_name'].widget.attrs.update({'class': 'form-input'})
        form.fields['username'].widget.attrs.update({'class': 'form-input'})
        form.fields['age'].widget.attrs.update({'class': 'form-input'})
        form.fields['email'].widget.attrs.update({'class': 'form-input'})
        return form

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['user'] = user
        g_def = self.get_user_context(title=context['user'])

        return dict(list(context.items()) + list(g_def.items()))

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     g_def = self.get_user_context(title="Регистрация")
    #     return dict(list(context.items()) + list(g_def.items()))



class EditUserProfile(DataMixin, ListView):
    model = CustomUser

    template_name = "books/edit_profile.html"

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     user = self.get_object()
    #     context['user'] = user
    #     g_def = self.get_user_context(title=context['user'])
    #
    #     return dict(list(context.items()) + list(g_def.items()))


def logout_user(request):
    logout(request)
    return redirect('login_user_page')


# РАБОТА С API

class BookAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 10000


class BookAPIList(generics.ListCreateAPIView):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = BookAPIListPagination


class BookAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    # permission_classes = (IsOwnerOrReadOnly, )
    permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication, )


class BookAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    permission_classes = (IsAdminOrReadOnly,)






# РАБОТА С API

# class BookViewSet(mixins.CreateModelMixin,
#                   mixins.RetrieveModelMixin,
#                   mixins.UpdateModelMixin,
#                   mixins.ListModelMixin,
#                   GenericViewSet):
#     # queryset = Books.objects.all()
#     serializer_class = BooksSerializer
#
#
#     def get_queryset(self):
#         pk = self.kwargs.get("pk")
#
#         if not pk:
#             return Books.objects.all()[:3]
#
#         return Books.objects.filter(pk=pk)
#
#     @action(methods=['get'], detail=True)
#     def genre(self, request, pk=None):
#         genres = Genres.objects.get(pk=pk)
#         return Response({'genres': genres.genre_name})

class BookAPIList(generics.ListCreateAPIView):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )


class BookAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    permission_classes = (IsOwnerOrReadOnly, )


class BookAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    permission_classes = (IsAdminOrReadOnly, )




def error404(request, exeption):
    return HttpResponseNotFound(f"<h1>Страница не найдена</h1>")


def error500(request):
    return HttpResponseNotFound("<h1>Ошибка сервера</h1>")


def error400(request, exeption):
    return HttpResponseNotFound("<h1>Некорректный запрос</h1>")


def error403(request, exeption):
    return HttpResponseNotFound("<h1>Доступ запрещен</h1>")
