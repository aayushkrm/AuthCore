from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Session
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserProfileSerializer,
    UserUpdateSerializer
)


class RegisterView(APIView):
    """
    POST /api/auth/register/
    Register a new user
    """
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'User registered successfully',
                'user_id': user.id,
                'email': user.email
            }, status=status.HTTP_201_CREATED)
        
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):
    """
    POST /api/auth/login/
    Authenticate user and return JWT token
    """
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        email = serializer.validated_data['email'].lower()
        password = serializer.validated_data['password']
        
        # Find user
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'error': 'Invalid credentials'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Check if account is active
        if not user.is_active:
            return Response(
                {'error': 'Account is deactivated'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Verify password
        if not user.check_password(password):
            return Response(
                {'error': 'Invalid credentials'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Generate JWT token
        token = user.generate_token()
        
        return Response({
            'token': token,
            'user_id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    POST /api/auth/logout/
    Logout user (mainly for session cleanup)
    """
    def post(self, request):
        if not hasattr(request, 'user') or request.user is None:
            return Response(
                {'error': 'Not authenticated'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # For JWT, client should remove token
        # For session-based, delete session here
        Session.objects.filter(user=request.user).delete()
        
        return Response(
            {'message': 'Logged out successfully'}, 
            status=status.HTTP_200_OK
        )


class ProfileView(APIView):
    """
    GET /api/auth/profile/
    Get current user profile
    """
    def get(self, request):
        if not hasattr(request, 'user') or request.user is None:
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        """
        PUT /api/auth/profile/
        Update current user profile
        """
        if not hasattr(request, 'user') or request.user is None:
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        serializer = UserUpdateSerializer(
            request.user, 
            data=request.data, 
            partial=True
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                UserProfileSerializer(request.user).data,
                status=status.HTTP_200_OK
            )
        
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request):
        """
        PATCH /api/auth/profile/
        Partial update current user profile
        """
        return self.put(request)


class DeleteAccountView(APIView):
    """
    DELETE /api/auth/delete-account/
    Soft delete user account
    """
    def delete(self, request):
        if not hasattr(request, 'user') or request.user is None:
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Soft delete - set is_active to False
        request.user.is_active = False
        request.user.save()
        
        # Delete all sessions
        Session.objects.filter(user=request.user).delete()
        
        return Response(
            {'message': 'Account deactivated successfully'}, 
            status=status.HTTP_200_OK
        )
