from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from recipes.utils import get_ingredients_new

urlpatterns = [
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path('admin/', admin.site.urls),
    path('ingredients/', get_ingredients_new, name='ingredients'),
    path("", include("recipes.urls")),
    path('about/', include('about.urls', namespace='about')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

handler404 = "recipes.views.page_not_found"
handler500 = "recipes.views.server_error"
