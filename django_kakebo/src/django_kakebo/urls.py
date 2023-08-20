from django.urls import path

from .views.kakebo import Index, SelectYearWeekFormView, KakeboWeekFormView

urlpatterns = [
    path("", Index.as_view(), name="kakebo-home"),
    path("calendar/", SelectYearWeekFormView.as_view(), name="kakebo-calendar"),
    path("calendar/<int:year>/", SelectYearWeekFormView.as_view(), name="kakebo-calendar"),
    path("calendar/<int:year>/<int:month>/", SelectYearWeekFormView.as_view(), name="kakebo-calendar"),
    path("<int:year>/<int:week>/", KakeboWeekFormView.as_view(), name="kakebo-week"),
]
