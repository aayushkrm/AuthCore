from rest_framework.response import Response
from rest_framework import status
from .models import AccessRoleRule, BusinessElement


class PermissionChecker:
    """
    Helper class to check permissions for users
    """
    
    @staticmethod
    def check_permission(user, element_name, action, obj=None):
        """
        Check if user has permission for action on element
        
        Args:
            user: User object
            element_name: Name of business element (e.g., 'products')
            action: Action to perform ('read', 'create', 'update', 'delete')
            obj: Optional object to check ownership
        
        Returns:
            tuple: (has_permission: bool, reason: str)
        """
        if not user or not user.is_active:
            return False, "User not authenticated"
        
        # Get business element
        try:
            element = BusinessElement.objects.get(name=element_name)
        except BusinessElement.DoesNotExist:
            return False, "Business element not found"
        
        # Get user roles
        user_roles = user.user_roles.all().values_list('role', flat=True)
        
        if not user_roles:
            return False, "User has no assigned roles"
        
        # Get access rules for user's roles
        rules = AccessRoleRule.objects.filter(
            role_id__in=user_roles,
            element=element
        )
        
        if not rules.exists():
            return False, "No permissions for this resource"
        
        # Check permissions based on action
        for rule in rules:
            if action == 'read':
                # Check read_all_permission first
                if rule.read_all_permission:
                    return True, "Access granted"
                # Then check read_permission with ownership
                if rule.read_permission:
                    if obj is None:
                        # For list views, read_permission without obj means can read own
                        return True, "Access granted"
                    if hasattr(obj, 'owner_id') and obj.owner_id == user.id:
                        return True, "Access granted"
            
            elif action == 'create':
                if rule.create_permission:
                    return True, "Access granted"
            
            elif action == 'update':
                # Check update_all_permission first
                if rule.update_all_permission:
                    return True, "Access granted"
                # Then check update_permission with ownership
                if rule.update_permission:
                    if obj and hasattr(obj, 'owner_id') and obj.owner_id == user.id:
                        return True, "Access granted"
            
            elif action == 'delete':
                # Check delete_all_permission first
                if rule.delete_all_permission:
                    return True, "Access granted"
                # Then check delete_permission with ownership
                if rule.delete_permission:
                    if obj and hasattr(obj, 'owner_id') and obj.owner_id == user.id:
                        return True, "Access granted"
        
        return False, "Insufficient permissions"

    @staticmethod
    def require_permission(element_name, action):
        """
        Decorator for views to check permissions
        
        Usage:
            @PermissionChecker.require_permission('products', 'create')
            def post(self, request):
                ...
        """
        def decorator(view_func):
            def wrapped_view(self, request, *args, **kwargs):
                if not hasattr(request, 'user') or request.user is None:
                    return Response(
                        {'error': 'Authentication required'}, 
                        status=status.HTTP_401_UNAUTHORIZED
                    )
                
                has_perm, reason = PermissionChecker.check_permission(
                    request.user, element_name, action
                )
                
                if not has_perm:
                    return Response(
                        {'error': reason}, 
                        status=status.HTTP_403_FORBIDDEN
                    )
                
                return view_func(self, request, *args, **kwargs)
            return wrapped_view
        return decorator

    @staticmethod
    def has_role(user, role_name):
        """
        Check if user has specific role
        
        Args:
            user: User object
            role_name: Name of role to check
        
        Returns:
            bool: True if user has role
        """
        if not user or not user.is_active:
            return False
        
        return user.user_roles.filter(role__name=role_name).exists()
