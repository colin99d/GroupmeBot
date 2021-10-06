"""Bot urls"""
__docformat__ = "numpy"

from django.urls import path, include
from . import views

urlpatterns = [
    path("", include(views.handler)),
]
