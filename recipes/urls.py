from django.urls import path

from . import api, views


urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new_recipe, name='recipe_new'),
    path('subscriptions', api.follow_add, name='follow_add'),
    path(
        'subscriptions/<int:author_id>',
        api.follow_delete,
        name='follow_delete',
    ),
    path('follow/', views.follow, name='follow'),
    path('favorites', api.favorite_add, name='favorite_add'),
    path(
        'favorites/<int:recipe_id>',
        api.favorite_delete,
        name='favorite_delete',
    ),
    path('favorite/', views.favorite, name='favorite'),
    path('purchases', api.shopping_list_add, name='shopping_list_add'),
    path(
        'purchases/<int:recipe_id>',
        api.shopping_list_delete,
        name='shopping_list_delete',
    ),
    path('shopping_list/', views.shopping_list, name='shopping_list'),
    path(
        'shopping_list/download/',
        views.shopping_list_download,
        name='shopping_list_download',
    ),
    path('<username>/', views.profile, name='profile'),
    path('<username>/<int:recipe_id>/', views.recipe, name='recipe'),
    path(
        '<username>/<int:recipe_id>/edit/',
        views.recipe_edit,
        name='recipe_edit',
    ),
    path(
        '<username>/<int:recipe_id>/delete/',
        views.recipe_delete,
        name='recipe_delete',
    ),
]
