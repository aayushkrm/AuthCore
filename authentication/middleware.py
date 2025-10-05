from django.utils.deprecation import MiddlewareMixin
from .models import User


class CustomAuthMiddleware(MiddlewareMixin):
    """
    Custom middleware to extract and validate JWT token from Authorization header
    Sets request.user if token is valid, otherwise sets it to None
    """
    
    def process_request(self, request):
        """
        Extract and validate JWT token from Authorization header
        """
        # Initialize user as None
        request.user = None
        
        # Get Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        # Check if Authorization header exists and starts with 'Bearer '
        if auth_header.startswith('Bearer '):
            # Extract token
            token = auth_header.split(' ')[1]
            
            # Decode token and get user_id
            user_id = User.decode_token(token)
            
            if user_id:
                # Try to get user from database
                try:
                    user = User.objects.get(id=user_id, is_active=True)
                    request.user = user
                except User.DoesNotExist:
                    # User not found or inactive
                    pass
        
        # Continue processing request
        return None
