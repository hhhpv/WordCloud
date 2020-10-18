# Hithesh
# URL Paths

from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views
from django.urls import re_path
from django.views.generic.base import RedirectView

urlpatterns = [
    path("generate/", views.generate, name="generate"),
    path("", views.index, name="index"),
]
