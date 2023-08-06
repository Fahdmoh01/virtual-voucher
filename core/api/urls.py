from django.urls import path
from .views import *

urlpatterns = [
    path("", OverviewAPI.as_view(), name="api-overview"),
]
