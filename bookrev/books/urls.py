from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *



urlpatterns = [
    path('', cache_page(60)(BookHome.as_view()), name="index"),
    path('book/<slug:book_slug>/', ShowBook.as_view(), name="show_book"),
    path('genre/<slug:genre_slug>/', cache_page(60)(BookGenre.as_view()), name='genre'),
    path('add/', AddBook.as_view(), name="add"),
    path('login/', Login.as_view(), name="login_user_page"),
    path('logout/', logout_user, name='logout_user_page'),
    path('register/', Register.as_view(), name="register"),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('<int:pk>/comment/', CommentCreateView.as_view(), name='create_comment'),
    path('<int:pk>/<int:com_pk>/comment_ans/', AnsCommentCreateView.as_view(), name='create_ans_comment'),
    path('user/<str:user_username>/', UserProfile.as_view(), name="profile"),
    path('user/<str:user_username>/editprofile', EditUserProfile.as_view(), name="edit_profile"),
]

