from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import UserRegistrationForm


class SignUp(CreateView):
    form_class = UserRegistrationForm
    success_url = reverse_lazy('recipes:index')
    template_name = 'registration/signup.html'
