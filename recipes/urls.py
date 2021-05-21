from django.urls import path

from . import views

urlpatterns = [
    path('favorite/', views.favorite, name='favorite'),
    path('follow/', views.follow_index, name='follow_index'),
    path('shopping-list/', views.shopping_list, name='shopping_list'),
    path('download_shopping_list/',
         views.download_shopping_list,
         name='download_shopping_list'),
    path('new/', views.new_recipe, name='new_recipe'),
    path('<str:username>/<int:recipe_id>/',
         views.recipe_view,
         name='recipe_view'),
    path('<str:username>/', views.profile, name='profile'),
    path(
        '<str:username>/<int:recipe_id>/edit/',
        views.recipe_edit,
        name='recipe_edit'
    ),
    path(
        '<str:username>/<int:recipe_id>/delete/',
        views.recipe_delete,
        name='recipe_delete'
    ),
    path('', views.index, name='index'),
]
