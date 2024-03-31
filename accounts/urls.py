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
    path("follow/<int:user_id>/", views.follow_user, name="follow")
]

app_name = 'accounts'
