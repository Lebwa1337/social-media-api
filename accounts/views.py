from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings

from accounts.permissions import ForeignProfileReadonly
from accounts.serializers import UserSerializer, AuthTokenSerializer, UploadImageSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class ObtainTokenView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = AuthTokenSerializer


class UserListViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

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
