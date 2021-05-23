from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    template_name = 'author.html'


class AboutTechView(TemplateView):
    template_name = 'tech.html'


class AboutSiteView(TemplateView):
    template_name = 'site_info.html'
