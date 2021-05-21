from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path
from django.views.static import serve

from recipes.views import page_not_found, server_error

handler404 = "recipes.views.page_not_found"  # noqa
handler500 = "recipes.views.server_error"  # noqa

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/', include('django.contrib.flatpages.urls')),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path("api/v1/", include('api.urls')),
    path("about-author/", views.flatpage, {"url": "/about-author/"},
         name="author"),
    path("about-spec/", views.flatpage, {"url": "/about-spec/"},
         name="spec"),
    path('food-assistant/', views.flatpage, {"url": "/food-assistant/"},
         name="food-assistant"),
    path("404/", page_not_found, name="page_not_found"),
    path("500/", server_error, name="server_error"),
    path('', include('recipes.urls')),
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

if not settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT}),
        url(r'^static/(?P<path>.*)$', serve,
            {'document_root': settings.STATIC_ROOT}),
    ]
