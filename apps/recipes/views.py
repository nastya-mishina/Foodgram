from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Exists, OuterRef
from django.http import FileResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView, View)
from django_filters.views import BaseFilterView

from foodgram import settings

from .filters import TaggedRecipeFilterSet
from .forms import RecipeForm
from .mixins import TagContextMixin
from .models import Favorite, Purchase, Recipe
from .permissions import AdminAuthorPermission
from .service import generate_pdf

User = get_user_model()


class IndexView(TagContextMixin, BaseFilterView, ListView):
    model = Recipe
    template_name = 'recipes/index.html'
    paginate_by = settings.PAGINATE_BY
    filterset_class = TaggedRecipeFilterSet

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.is_authenticated:
            queryset = queryset.annotate(
                is_favorites=Exists(
                    Favorite.objects.filter(
                        user=self.request.user,
                        recipe=OuterRef('pk'),
                    ),
                ),
            ).annotate(
                is_purchase=Exists(
                    Purchase.objects.filter(
                        user=self.request.user,
                        recipe=OuterRef('pk'),
                    ),
                ),
            )
        return queryset


class FollowView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'recipes/follow.html'
    paginate_by = settings.PAGINATE_BY
    queryset = User.objects.all()

    def get_queryset(self):
        return FollowView.queryset.filter(
            followers__user=self.request.user).order_by('-id')


class FavoriteView(TagContextMixin, LoginRequiredMixin,
                   BaseFilterView, ListView):
    model = Recipe
    template_name = 'recipes/favorites.html'
    paginate_by = settings.PAGINATE_BY
    filterset_class = TaggedRecipeFilterSet
    queryset = Recipe.objects.all()

    def get_queryset(self):
        return FavoriteView.queryset.filter(
            in_favorites__user=self.request.user)


class ProfileView(TagContextMixin, BaseFilterView, ListView):
    model = Recipe
    template_name = 'recipes/profile.html'
    paginate_by = settings.PAGINATE_BY
    filterset_class = TaggedRecipeFilterSet
    queryset = Recipe.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = get_object_or_404(User, username=self.kwargs['username'])
        is_follower = False
        if self.request.user.is_authenticated:
            is_follower = self.request.user.followers.filter(
                author=author).exists()
        context.update(
            {
                'user_is_follower': is_follower,
                'author': author,
            }
        )
        return context

    def get_queryset(self):
        author = get_object_or_404(User, username=self.kwargs['username'])
        return ProfileView.queryset.filter(author=author)


class RecipeView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe.html'


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    template_name = 'recipes/add_recipe.html'
    form_class = RecipeForm
    success_url = reverse_lazy('recipes:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    permission_classes = AdminAuthorPermission
    template_name = 'recipes/add_recipe.html'
    form_class = RecipeForm
    success_url = reverse_lazy('recipes:index')


class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipe
    permission_classes = AdminAuthorPermission
    success_url = reverse_lazy('recipes:purchases')


class PurchaseView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/purchases.html'
    queryset = Recipe.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['object_list'] = self.get_user_purchase()
        return context

    def get_user_purchase(self):
        return PurchaseView.queryset.filter(
            in_purchases__user=self.request.user)


class DownloadPurchasesListView(View):
    def get(self, request, *args, **kwargs):
        pdf = generate_pdf(request.user)

        return FileResponse(
            pdf,
            as_attachment=True,
            filename='purchases.pdf',
        )


@login_required
def get_purchases_count(request):
    """
    Shopping List.
    """
    recipes = request.user.purchases.all()
    return render(
        request,
        {'recipes': recipes},
    )
