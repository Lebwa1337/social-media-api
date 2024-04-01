from django.urls import path

from accounts import views

urlpatterns = [
    path("register/", views.CreateUserView.as_view(), name="register"),
    path("login/", views.ObtainTokenView.as_view(), name="login"),
    path("profiles/", views.UserListViewSet.as_view(
        {"get": "list"}
    ),
         name="profiles"
         ),
    path("profile/<int:pk>/", views.ManageUserViewSet.as_view(
        {
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update"
        }
    ),
         name="me"
         ),
    path("logout/", views.user_logout, name="logout"),
    path("follow/", views.follow_user, name="follow"),
    path("unfollow/", views.unfollow_user, name="unfollow"),
    path(
        "posts/",
        views.PostViewSet.as_view(
            {
                "get": "list",
                "post": "create",
                "delete": "destroy"
            }
        ),
        name="post"
    )
]

app_name = 'accounts'
