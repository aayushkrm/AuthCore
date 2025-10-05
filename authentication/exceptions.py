from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import PermissionDenied
from django.http import Http404


def custom_exception_handler(exc, context):
    """
    Custom exception handler for consistent error responses across the API
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    # If response exists, customize the error format
    if response is not None:
        custom_response_data = {
            'error': response.data.get('detail', str(exc)),
            'status_code': response.status_code
        }
        
        # If there are field-specific errors, include them
        if isinstance(response.data, dict) and 'detail' not in response.data:
            custom_response_data['errors'] = response.data
        
        response.data = custom_response_data
    else:
        # Handle exceptions not caught by DRF
        if isinstance(exc, Http404):
            return Response(
                {
                    'error': 'Resource not found',
                    'status_code': 404
                },
                status=status.HTTP_404_NOT_FOUND
            )
        elif isinstance(exc, PermissionDenied):
            return Response(
                {
                    'error': 'Permission denied',
                    'status_code': 403
                },
                status=status.HTTP_403_FORBIDDEN
            )
        else:
            # Generic server error
            return Response(
                {
                    'error': 'Internal server error',
                    'status_code': 500
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    return response
