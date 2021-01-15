from django.contrib.auth import login
from django.contrib.auth.models import User
from django.views.generic import TemplateView

from public.utils import USERNAME


class AuthenticatedView(TemplateView):
    """
    The purpose of this view is to prove that
    we're using session authorization properly
    by authenticating immediately.
    """
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        login(self.request, User.objects.get(username=USERNAME))
