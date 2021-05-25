from django.conf import settings
from django.conf.urls import handler404, handler500
from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path

handler404 = 'foodgram.views.page_not_found'  # noqa
handler500 = 'foodgram.views.server_error'  # noqa


flatpages_urls = [
    path('pages/', include('django.contrib.flatpages.urls')),
    path('author/', views.flatpage, {'url': '/author/'}, name='about_author'),
    path('tech/', views.flatpage, {'url': '/tech/'}, name='about_tech'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('apps.users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('api/', include('apps.api.urls')),
    path('about/', include(flatpages_urls)),
    path('', include('apps.recipes.urls', namespace='recipes')),
]


if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
