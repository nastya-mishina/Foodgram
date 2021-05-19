from django.urls import path

from . import views

urlpatterns = [
    path('ingredients/', views.get_ingredients, name='ingredients'),
    path('favorites/', views.favorite_add, name='favorite_add'),
    path('favorites/<int:recipe_id>/', views.favorite_delete, name='favorite_delete'),
    path('follow/', views.follow_add, name='follow'),
    path('unfollow/<int:author_id>/', views.follow_delete, name='unfollow'),
    path('shopping_list_add/', views.shopping_list_add, name='shopping_list_add'),
    path('shopping_list_delete/<int:recipe_id>/', views.shopping_list_delete, name='shopping_list_delete'),
]
