from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('ingredients', views.IngredientApiView)
router.register('favorites', views.FavoriteApiView)
router.register('subscriptions', views.FollowApiView)
router.register('purchases', views.PurchaseApiView)


urlpatterns = [
    path('v1/', include(router.urls)),
]
