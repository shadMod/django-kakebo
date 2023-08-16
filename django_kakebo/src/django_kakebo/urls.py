from django.urls import path

from .views.kakebo import Index, KakeboWeekFormView

urlpatterns = [
    path("", Index.as_view(), name="kakebo-home"),
    path("<int:year>/<int:week>", KakeboWeekFormView.as_view(), name="kakebo-week"),
]
