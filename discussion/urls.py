from django.urls import path
from . import views

urlpatterns = [
    path("<int:classpk>", views.GetClassDiscussions.as_view()),
    path("<int:pk>/response", views.GetDiscussionResponses.as_view()),
    path("<int:pk>/solved", views.MarkDiscussionSolved.as_view())
]
