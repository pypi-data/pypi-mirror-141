from rest_framework.generics import UpdateAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import views, status, permissions
from rest_framework.response import Response

from .serializers import UserCreateSerializer, UserSerializer, PasswordChangeSerializer
from .models import User
from .response import prepare_create_success_response, prepare_success_response, prepare_error_response
from .services import register_user_validate


# User Registration
class CreateUserView(views.APIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        validate_error = register_user_validate(request.data)
        if validate_error is not None:
            return Response(prepare_error_response(validate_error), status=status.HTTP_400_BAD_REQUEST)
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(prepare_create_success_response(serializer.data), status=status.HTTP_201_CREATED)
        return Response(prepare_error_response(serializer.errors), status=status.HTTP_400_BAD_REQUEST)


# User Login
class LoginAPIView(ObtainAuthToken):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        token, created = Token.objects.get_or_create(user=serializer.validated_data['user'])
        user = serializer.validated_data['user']
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'message': 'The user has been login successfully'
        }, status=status.HTTP_200_OK)


# User Profile
class ProfileView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            queryset = User.objects.get(id=self.request.user.id)
            serializer = UserSerializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(prepare_error_response('Sorry! User must be login'), status=status.HTTP_400_BAD_REQUEST)


# Profile update
class ProfileUpdateView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return User.objects.filter(id=pk).first()
        except User.DoesNotExist:
            return None

    def put(self, request, pk):
        user = self.get_object(pk)
        if user is not None:
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(prepare_create_success_response(serializer.data), status=status.HTTP_201_CREATED)
            return Response(prepare_error_response(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(prepare_error_response("No user found for this ID"), status=status.HTTP_400_BAD_REQUEST)


# Change Password
class ChangePasswordView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PasswordChangeSerializer


# Logout
class LogoutView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        request.user.auth_token.delete()
        return Response(prepare_success_response("User has been logout"), status=status.HTTP_200_OK)
