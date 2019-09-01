from django.conf.urls import url
from .views import CreateUserAPIView, authenticate_user

urlpatterns = [
    url(r'^signup/$', CreateUserAPIView.as_view()),
    url(r'^login/$', authenticate_user)
]
