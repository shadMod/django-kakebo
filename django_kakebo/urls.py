from .src.django_kakebo.urls import urlpatterns as urlpatterns_kakebo
from .src.user.urls import urlpatterns as urlpatterns_user

urlpatterns = []
urlpatterns.extend(urlpatterns_kakebo)
urlpatterns.extend(urlpatterns_user)
