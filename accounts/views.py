from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics, permissions, status, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings

from accounts.models import Follow, User, Post
from accounts.permissions import ForeignProfileReadonly
from accounts.serializers import (
    UserSerializer,
    AuthTokenSerializer,
    UploadImageSerializer,
    PostSerializer
)


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class ObtainTokenView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = AuthTokenSerializer


class UserListViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="email",
                type=OpenApiTypes.EMAIL,
                description="Filter users by email address"
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = get_user_model().objects.all()
        email = self.request.query_params.get('email')
        if email:
            queryset = queryset.filter(email__icontains=email)
        return queryset


class ManageUserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [ForeignProfileReadonly]

    def get_object(self):
        obj = get_user_model().objects.get(id=self.kwargs["pk"])
        return obj

    def get_serializer_class(self):
        if self.action == "upload_image":
            return UploadImageSerializer
        return UserSerializer

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
        permission_classes=[permissions.IsAuthenticated]
    )
    def upload_image(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'POST':
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request):
    user_id = request.data["user_id"]
    user_to_follow = get_object_or_404(User, id=user_id)
    if not request.user.follower.filter(following__id=user_id).exists():
        Follow.objects.create(follower=request.user, following=user_to_follow)
        return Response(
            {"message": "Your are currently following {}".format(user_to_follow.email)},
            status=status.HTTP_200_OK
        )
    return Response(
        {"message": "Your are already following {}".format(user_to_follow.email)},
        status=status.HTTP_202_ACCEPTED
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request):
    user_id = request.data["user_id"]
    user_to_unfollow = get_object_or_404(User, id=user_id)
    request.user.follower.filter(following__id=user_id).delete()
    return Response(
            {"message": "Successfully unfollowing {}".format(user_to_unfollow.email)},
            status=status.HTTP_200_OK
        )


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="followers",
                type=OpenApiTypes.BOOL,
                description="Show posts of users who you follow"
            ),
            OpenApiParameter(
                name="title",
                type=OpenApiTypes.STR,
                description="Filter posts by title"
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        followers = self.request.query_params.get('followers')
        title = self.request.query_params.get('title')
        if not followers:
            queryset = Post.objects.filter(user=self.request.user)
        else:
            queryset = Post.objects.all()
        if followers:
            """Getting id`s of users, who authenticated user is following"""
            following_id = []
            for follow_instance in self.request.user.follower.all():
                following_id.append(follow_instance.following.id)
            queryset = queryset.filter(user__id__in=following_id)
        if title:
            queryset = queryset.filter(title__icontains=title)
        return queryset
