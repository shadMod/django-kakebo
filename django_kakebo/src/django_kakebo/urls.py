from django.urls import path

from .views import Index, KakeboWeekFormView

urlpatterns = [
    path("", Index.as_view(), name="kakebo-home"),
    path("<str:username>/<int:year>/<int:week>", KakeboWeekFormView.as_view(), name="kakebo-week"),
]
