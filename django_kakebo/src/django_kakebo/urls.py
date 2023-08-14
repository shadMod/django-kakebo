from django.urls import path

from .views import Index, KakeboWeek

urlpatterns = [
    path("", Index.as_view(), name="kakebo-home"),
    path("<str:username>/<int:year>/<int:week>", KakeboWeek.as_view(), name="kakebo-week"),
]
