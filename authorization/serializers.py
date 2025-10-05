from rest_framework import serializers
from .models import Role, BusinessElement, AccessRoleRule, UserRole


class RoleSerializer(serializers.ModelSerializer):
    """Serializer for Role model"""
    class Meta:
        model = Role
        fields = ['id', 'name', 'description']


class BusinessElementSerializer(serializers.ModelSerializer):
    """Serializer for BusinessElement model"""
    class Meta:
        model = BusinessElement
        fields = ['id', 'name', 'description']


class AccessRuleSerializer(serializers.ModelSerializer):
    """Serializer for AccessRoleRule model"""
    role_name = serializers.CharField(source='role.name', read_only=True)
    element_name = serializers.CharField(source='element.name', read_only=True)
    
    class Meta:
        model = AccessRoleRule
        fields = [
            'id', 
            'role', 
            'role_name', 
            'element', 
            'element_name',
            'read_permission', 
            'read_all_permission', 
            'create_permission',
            'update_permission', 
            'update_all_permission', 
            'delete_permission', 
            'delete_all_permission'
        ]

    def validate(self, data):
        """Validate that role and element exist"""
        role = data.get('role')
        element = data.get('element')
        
        # Check if rule already exists (for POST only)
        if self.instance is None:  # Creating new rule
            if AccessRoleRule.objects.filter(role=role, element=element).exists():
                raise serializers.ValidationError(
                    "Access rule for this role and element already exists"
                )
        
        return data


class UserRoleSerializer(serializers.ModelSerializer):
    """Serializer for UserRole model"""
    role_name = serializers.CharField(source='role.name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = UserRole
        fields = [
            'id', 
            'user', 
            'user_email', 
            'role', 
            'role_name', 
            'assigned_at'
        ]
