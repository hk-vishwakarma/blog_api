from django.urls import path

from .views import (
    PostListCreateView,
    PostCommentsView,
    HealthView,
    ReadinessView,
    SignupView
)


urlpatterns = [
    path("posts/", PostListCreateView.as_view(), name="posts"),
    path(
        "posts/<int:pk>/comments/",
        PostCommentsView.as_view(),
        name="post-comments",
    ),
    path("health/", HealthView.as_view(), name="health"),
    path("readiness/", ReadinessView.as_view(), name="readiness"),
    path("api/signup/", SignupView.as_view(), name="signup"),
]