import types

from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from rest_framework.response import Response

from apps.recipes.models import Favorite, Ingredient, Purchase
from apps.users.models import Follow

from . import serializers

SUCCESS = types.MappingProxyType({'success': True})
UNSUCCESS = types.MappingProxyType({'success': False})


class BaseInstanceView(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(SUCCESS)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        is_deleted = instance.delete()
        if is_deleted:
            return Response(SUCCESS)
        return Response(UNSUCCESS)


class IngredientApiView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('title',)


class FollowApiView(BaseInstanceView):
    queryset = Follow.objects.all()
    serializer_class = serializers.FollowSerializer

    def get_object(self):
        instance = get_object_or_404(
            FollowApiView.queryset,
            user=self.request.user,
            author=self.kwargs['pk'],
        )
        self.check_object_permissions(self.request, instance)
        return instance


class FavoriteApiView(BaseInstanceView):
    queryset = Favorite.objects.all()
    serializer_class = serializers.FavoriteSerializer

    def get_object(self):
        instance = get_object_or_404(
            Favorite,
            user=self.request.user,
            recipe=self.kwargs['pk'],
        )
        return instance


class PurchaseApiView(mixins.ListModelMixin, BaseInstanceView):
    queryset = Purchase.objects.all()
    serializer_class = serializers.PurchaseSerializer

    def get_object(self):
        instance = get_object_or_404(
            PurchaseApiView.queryset,
            user=self.request.user,
            recipe=self.kwargs['pk'],
        )
        self.check_object_permissions(self.request, instance)
        return instance
