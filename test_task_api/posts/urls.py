from django.conf.urls import url

from posts.views import CreatePostAPIView, LikePostAPIView, UnlikePostAPIView, ListOfPostsAPIView

urlpatterns = [
    url(r'^creation/$', CreatePostAPIView.as_view()),
    url(r'^like/$', LikePostAPIView.as_view()),
    url(r'^unlike/$', UnlikePostAPIView.as_view()),
    url(r'^list/$', ListOfPostsAPIView.as_view())
]
