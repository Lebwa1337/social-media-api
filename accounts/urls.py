from django.urls import path

from accounts.views import (
    CreateUserView,
    ObtainTokenView,
    UserListViewSet,
    ManageUserViewSet,
    user_logout,
    follow_user,
    unfollow_user,
    PostViewSet
)

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("login/", ObtainTokenView.as_view(), name="login"),
    path("profiles/", UserListViewSet.as_view(
        {"get": "list"}
    ),
         name="profiles"
         ),
    path("profile/<int:pk>/", ManageUserViewSet.as_view(
        {
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update"
        }
    ),
         name="me"
         ),
    path("logout/", user_logout, name="logout"),
    path("follow/", follow_user, name="follow"),
    path("unfollow/", unfollow_user, name="unfollow"),
    path(
        "posts/",
        PostViewSet.as_view(
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
