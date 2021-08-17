from django.urls import include, path
from rest_framework.routers import DefaultRouter

from Task.Program.views import View

router = DefaultRouter()

router.register(r'url',View)
urlpatterns = [
    path('', include(router.urls)),
    path('address/<str:address>/',View.as_view({"get":"address"}))
]