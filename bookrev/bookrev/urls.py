"""bookrev URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
import debug_toolbar

from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView, TokenVerifyView

from bookrev import settings
from rest_framework import routers
from books.views import *




# class MyCustomRouter(routers.SimpleRouter):
#     routes = [
#         routers.Route(url=r'^{prefix}$',
#                       mapping={'get': 'list'},
#                       name='{basename}-list',
#                       detail=False,
#                       initkwargs={'suffix': 'List'}),
#         routers.Route(url=r'^{prefix}/{lookup}$',
#                       mapping={'get': 'retrieve'},
#                       name='{basename}-detail',
#                       detail=True,
#                       initkwargs={'suffix': 'Detail'})
#     ]
#
#
# router = MyCustomRouter()
# router.register(r'book', BookViewSet, basename='books')
# print(router.urls)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
    path('', include('books.urls')),
    path('api/v1/book/', BookAPIList.as_view()),
    path('api/v1/book/<int:pk>/', BookAPIUpdate.as_view()),
    path('api/v1/bookdelete/<int:pk>/', BookAPIDestroy.as_view()),
    path('api/v1/drf-auth/', include('rest_framework.urls')),
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/refresh/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/v1/bookdelete/<int:pk>/', BookAPIDestroy.as_view())
    # path('api/v1/', include(router.urls))
]

if settings.DEBUG:

    urlpatterns = [
        path('__debug__/', include('debug_toolbar.urls')),
    ] + urlpatterns

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = error404
handler500 = error500
handler400 = error400
handler403 = error403
