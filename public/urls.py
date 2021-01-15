from django.urls import path
from django.views.generic import TemplateView

from public.views import AuthenticatedView


app_name = "public"
urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html")),
    path("authenticated/", AuthenticatedView.as_view()),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt")),
    path("logo192.png", TemplateView.as_view(template_name="logo192.png")),
    path("logo512.png", TemplateView.as_view(template_name="logo512.png")),
    path("favicon.ico", TemplateView.as_view(template_name="favicon.ico")),
    path("manifest.json", TemplateView.as_view(template_name="manifest.json")),
]
