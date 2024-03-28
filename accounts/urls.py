from django.urls import path

from accounts import views

urlpatterns = [
    path("register/", views.CreateUserView.as_view(), name="register"),
    path("login/", views.ObtainTokenView.as_view(), name="login"),
    path("me/", views.ManageUserViewSet.as_view(
        {
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update"
         }
    ),
         name="me"
         ),
    path("logout/", views.user_logout, name="logout")
]

app_name = 'accounts'
