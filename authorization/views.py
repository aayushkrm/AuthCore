from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import AccessRoleRule, Role, BusinessElement
from .serializers import AccessRuleSerializer, RoleSerializer, BusinessElementSerializer
from .permissions import PermissionChecker


class AccessRulesListCreateView(APIView):
    """
    GET /api/access-rules/ - List all access rules (admin only)
    POST /api/access-rules/ - Create new access rule (admin only)
    """
    
    def get(self, request):
        """List all access rules"""
        # Check authentication
        if not hasattr(request, 'user') or request.user is None:
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Check admin role
        if not PermissionChecker.has_role(request.user, 'admin'):
            return Response(
                {'error': 'Admin access required'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        rules = AccessRoleRule.objects.all()
        serializer = AccessRuleSerializer(rules, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create new access rule"""
        # Check authentication
        if not hasattr(request, 'user') or request.user is None:
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Check admin role
        if not PermissionChecker.has_role(request.user, 'admin'):
            return Response(
                {'error': 'Admin access required'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = AccessRuleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccessRuleDetailView(APIView):
    """
    GET /api/access-rules/{id}/ - Get specific access rule (admin only)
    PUT /api/access-rules/{id}/ - Update access rule (admin only)
    DELETE /api/access-rules/{id}/ - Delete access rule (admin only)
    """
    
    def get_object(self, pk):
        """Helper method to get access rule object"""
        try:
            return AccessRoleRule.objects.get(pk=pk)
        except AccessRoleRule.DoesNotExist:
            return None

    def get(self, request, pk):
        """Get specific access rule"""
        # Check authentication and admin role
        if not request.user or not PermissionChecker.has_role(request.user, 'admin'):
            return Response(
                {'error': 'Admin access required'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        rule = self.get_object(pk)
        if not rule:
            return Response(
                {'error': 'Access rule not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = AccessRuleSerializer(rule)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """Update access rule"""
        # Check authentication and admin role
        if not request.user or not PermissionChecker.has_role(request.user, 'admin'):
            return Response(
                {'error': 'Admin access required'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        rule = self.get_object(pk)
        if not rule:
            return Response(
                {'error': 'Access rule not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = AccessRuleSerializer(rule, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """Partial update access rule"""
        return self.put(request, pk)

    def delete(self, request, pk):
        """Delete access rule"""
        # Check authentication and admin role
        if not request.user or not PermissionChecker.has_role(request.user, 'admin'):
            return Response(
                {'error': 'Admin access required'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        rule = self.get_object(pk)
        if not rule:
            return Response(
                {'error': 'Access rule not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        rule.delete()
        return Response(
            {'message': 'Access rule deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )


class RolesListView(APIView):
    """
    GET /api/roles/ - List all roles (admin only)
    """
    
    def get(self, request):
        """List all roles"""
        if not request.user or not PermissionChecker.has_role(request.user, 'admin'):
            return Response(
                {'error': 'Admin access required'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BusinessElementsListView(APIView):
    """
    GET /api/business-elements/ - List all business elements (admin only)
    """
    
    def get(self, request):
        """List all business elements"""
        if not request.user or not PermissionChecker.has_role(request.user, 'admin'):
            return Response(
                {'error': 'Admin access required'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        elements = BusinessElement.objects.all()
        serializer = BusinessElementSerializer(elements, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
