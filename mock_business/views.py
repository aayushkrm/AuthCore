from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from authorization.permissions import PermissionChecker
from authorization.models import AccessRoleRule, BusinessElement


# ==================== MOCK DATA STORAGE ====================

MOCK_PRODUCTS = {
    1: {'id': 1, 'name': 'Laptop', 'price': 1200, 'category': 'Electronics', 'owner_id': 1},
    2: {'id': 2, 'name': 'Mouse', 'price': 25, 'category': 'Electronics', 'owner_id': 1},
    3: {'id': 3, 'name': 'Keyboard', 'price': 75, 'category': 'Electronics', 'owner_id': 2},
    4: {'id': 4, 'name': 'Monitor', 'price': 300, 'category': 'Electronics', 'owner_id': 3},
}

MOCK_ORDERS = {
    1: {'id': 1, 'product_id': 1, 'quantity': 2, 'total': 2400, 'status': 'pending', 'owner_id': 1},
    2: {'id': 2, 'product_id': 2, 'quantity': 5, 'total': 125, 'status': 'completed', 'owner_id': 2},
    3: {'id': 3, 'product_id': 3, 'quantity': 1, 'total': 75, 'status': 'shipped', 'owner_id': 3},
}

MOCK_STORES = {
    1: {'id': 1, 'name': 'Main Store', 'address': '123 Main St', 'city': 'New York', 'owner_id': 1},
    2: {'id': 2, 'name': 'Downtown Branch', 'address': '456 Market St', 'city': 'San Francisco', 'owner_id': 2},
    3: {'id': 3, 'name': 'Suburb Location', 'address': '789 Oak Ave', 'city': 'Chicago', 'owner_id': 1},
}

MOCK_USERS_DATA = {
    1: {'id': 1, 'email': 'admin@test.com', 'first_name': 'Admin', 'last_name': 'User', 'role': 'admin'},
    2: {'id': 2, 'email': 'user1@test.com', 'first_name': 'John', 'last_name': 'Doe', 'role': 'user'},
    3: {'id': 3, 'email': 'user2@test.com', 'first_name': 'Jane', 'last_name': 'Smith', 'role': 'user'},
}


# ==================== HELPER CLASSES AND FUNCTIONS ====================

class MockObject:
    """Helper class to simulate model objects with owner_id"""
    def __init__(self, data):
        for key, value in data.items():
            setattr(self, key, value)


def check_list_permission(request, element_name, mock_data):
    """
    Helper to filter list based on permissions
    Returns: (filtered_data, error_response)
    """
    if not request.user:
        return None, Response(
            {'error': 'Authentication required'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    user_roles = request.user.user_roles.all().values_list('role', flat=True)
    
    try:
        element = BusinessElement.objects.get(name=element_name)
    except BusinessElement.DoesNotExist:
        return None, Response(
            {'error': 'Business element not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    rules = AccessRoleRule.objects.filter(role_id__in=user_roles, element=element)
    
    if not rules.exists():
        return None, Response(
            {'error': 'No permissions for this resource'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    has_read_all = any(rule.read_all_permission for rule in rules)
    has_read_own = any(rule.read_permission for rule in rules)
    
    if not has_read_all and not has_read_own:
        return None, Response(
            {'error': 'Insufficient permissions'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    if has_read_all:
        return list(mock_data.values()), None
    else:
        # Only return items owned by current user
        return [
            item for item in mock_data.values() 
            if item.get('owner_id') == request.user.id
        ], None


# ==================== PRODUCTS ENDPOINTS ====================

class ProductListView(APIView):
    """
    GET /api/products/ - List products (filtered by permissions)
    POST /api/products/ - Create new product
    """
    
    def get(self, request):
        """List products based on user permissions"""
        result, error = check_list_permission(request, 'products', MOCK_PRODUCTS)
        if error:
            return error
        return Response(result, status=status.HTTP_200_OK)

    def post(self, request):
        """Create new product"""
        if not request.user:
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        has_perm, reason = PermissionChecker.check_permission(
            request.user, 'products', 'create'
        )
        if not has_perm:
            return Response(
                {'error': reason}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Create new product
        new_id = max(MOCK_PRODUCTS.keys()) + 1 if MOCK_PRODUCTS else 1
        new_product = {
            'id': new_id,
            'name': request.data.get('name'),
            'price': request.data.get('price'),
            'category': request.data.get('category', 'Uncategorized'),
            'owner_id': request.user.id
        }
        MOCK_PRODUCTS[new_id] = new_product
        
        return Response(new_product, status=status.HTTP_201_CREATED)


class ProductDetailView(APIView):
    """
    GET /api/products/{id}/ - Get single product
    PUT /api/products/{id}/ - Update product
    DELETE /api/products/{id}/ - Delete product
    """
    
    def get(self, request, pk):
        """Get single product"""
        if not request.user:
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if pk not in MOCK_PRODUCTS:
            return Response(
                {'error': 'Product not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        product_data = MOCK_PRODUCTS[pk]
        mock_obj = MockObject(product_data)
        
        has_perm, reason = PermissionChecker.check_permission(
            request.user, 'products', 'read', mock_obj
        )
        if not has_perm:
            return Response(
                {'error': reason}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        return Response(product_data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """Update product"""
        if not request.user:
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if pk not in MOCK_PRODUCTS:
            return Response(
                {'error': 'Product not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        product_data = MOCK_PRODUCTS[pk]
        mock_obj = MockObject(product_data)
        
        has_perm, reason = PermissionChecker.check_permission(
            request.user, 'products', 'update', mock_obj
        )
        if not has_perm:
            return Response(
                {'error': reason}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Update product
        product_data.update({
            'name': request.data.get('name', product_data['name']),
            'price': request.data.get('price', product_data['price']),
            'category': request.data.get('category', product_data['category']),
        })
        
        return Response(product_data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        """Partial update product"""
        return self.put(request, pk)

    def delete(self, request, pk):
        """Delete product"""
        if not request.user:
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if pk not in MOCK_PRODUCTS:
            return Response(
                {'error': 'Product not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        product_data = MOCK_PRODUCTS[pk]
        mock_obj = MockObject(product_data)
        
        has_perm, reason = PermissionChecker.check_permission(
            request.user, 'products', 'delete', mock_obj
        )
        if not has_perm:
            return Response(
                {'error': reason}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        del MOCK_PRODUCTS[pk]
        return Response(status=status.HTTP_204_NO_CONTENT)


# ==================== ORDERS ENDPOINTS ====================

class OrderListView(APIView):
    """
    GET /api/orders/ - List orders (filtered by permissions)
    POST /api/orders/ - Create new order
    """
    
    def get(self, request):
        """List orders based on user permissions"""
        result, error = check_list_permission(request, 'orders', MOCK_ORDERS)
        if error:
            return error
        return Response(result, status=status.HTTP_200_OK)

    def post(self, request):
        """Create new order"""
        if not request.user:
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        has_perm, reason = PermissionChecker.check_permission(
            request.user, 'orders', 'create'
        )
        if not has_perm:
            return Response(
                {'error': reason}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        new_id = max(MOCK_ORDERS.keys()) + 1 if MOCK_ORDERS else 1
        new_order = {
            'id': new_id,
            'product_id': request.data.get('product_id'),
            'quantity': request.data.get('quantity'),
            'total': request.data.get('total'),
            'status': request.data.get('status', 'pending'),
            'owner_id': request.user.id
        }
        MOCK_ORDERS[new_id] = new_order
        
        return Response(new_order, status=status.HTTP_201_CREATED)


class OrderDetailView(APIView):
    """
    GET /api/orders/{id}/ - Get single order
    PUT /api/orders/{id}/ - Update order
    DELETE /api/orders/{id}/ - Delete order
    """
    
    def get(self, request, pk):
        """Get single order"""
        if not request.user:
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if pk not in MOCK_ORDERS:
            return Response(
                {'error': 'Order not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        order_data = MOCK_ORDERS[pk]
        mock_obj = MockObject(order_data)
        
        has_perm, reason = PermissionChecker.check_permission(
            request.user, 'orders', 'read', mock_obj
        )
        if not has_perm:
            return Response(
                {'error': reason}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        return Response(order_data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """Update order"""
        if not request.user:
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if pk not in MOCK_ORDERS:
            return Response(
                {'error': 'Order not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        order_data = MOCK_ORDERS[pk]
        mock_obj = MockObject(order_data)
        
        has_perm, reason = PermissionChecker.check_permission(
            request.user, 'orders', 'update', mock_obj
        )
        if not has_perm:
            return Response(
                {'error': reason}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        order_data.update({
            'quantity': request.data.get('quantity', order_data['quantity']),
            'status': request.data.get('status', order_data['status']),
            'total': request.data.get('total', order_data['total']),
        })
        
        return Response(order_data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        """Partial update order"""
        return self.put(request, pk)

    def delete(self, request, pk):
        """Delete order"""
        if not request.user:
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if pk not in MOCK_ORDERS:
            return Response(
                {'error': 'Order not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        order_data = MOCK_ORDERS[pk]
        mock_obj = MockObject(order_data)
        
        has_perm, reason = PermissionChecker.check_permission(
            request.user, 'orders', 'delete', mock_obj
        )
        if not has_perm:
            return Response(
                {'error': reason}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        del MOCK_ORDERS[pk]
        return Response(status=status.HTTP_204_NO_CONTENT)


# ==================== STORES ENDPOINTS ====================

class StoreListView(APIView):
    """
    GET /api/stores/ - List stores (filtered by permissions)
    POST /api/stores/ - Create new store
    """
    
    def get(self, request):
        """List stores based on user permissions"""
        result, error = check_list_permission(request, 'stores', MOCK_STORES)
        if error:
            return error
        return Response(result, status=status.HTTP_200_OK)

    def post(self, request):
        """Create new store"""
        if not request.user:
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        has_perm, reason = PermissionChecker.check_permission(
            request.user, 'stores', 'create'
        )
        if not has_perm:
            return Response(
                {'error': reason}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        new_id = max(MOCK_STORES.keys()) + 1 if MOCK_STORES else 1
        new_store = {
            'id': new_id,
            'name': request.data.get('name'),
            'address': request.data.get('address'),
            'city': request.data.get('city'),
            'owner_id': request.user.id
        }
        MOCK_STORES[new_id] = new_store
        
        return Response(new_store, status=status.HTTP_201_CREATED)


class StoreDetailView(APIView):
    """
    GET /api/stores/{id}/ - Get single store
    PUT /api/stores/{id}/ - Update store
    DELETE /api/stores/{id}/ - Delete store
    """
    
    def get(self, request, pk):
        """Get single store"""
        if not request.user:
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if pk not in MOCK_STORES:
            return Response(
                {'error': 'Store not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        store_data = MOCK_STORES[pk]
        mock_obj = MockObject(store_data)
        
        has_perm, reason = PermissionChecker.check_permission(
            request.user, 'stores', 'read', mock_obj
        )
        if not has_perm:
            return Response(
                {'error': reason}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        return Response(store_data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """Update store"""
        if not request.user:
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if pk not in MOCK_STORES:
            return Response(
                {'error': 'Store not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        store_data = MOCK_STORES[pk]
        mock_obj = MockObject(store_data)
        
        has_perm, reason = PermissionChecker.check_permission(
            request.user, 'stores', 'update', mock_obj
        )
        if not has_perm:
            return Response(
                {'error': reason}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        store_data.update({
            'name': request.data.get('name', store_data['name']),
            'address': request.data.get('address', store_data['address']),
            'city': request.data.get('city', store_data['city']),
        })
        
        return Response(store_data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        """Partial update store"""
        return self.put(request, pk)

    def delete(self, request, pk):
        """Delete store"""
        if not request.user:
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if pk not in MOCK_STORES:
            return Response(
                {'error': 'Store not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        store_data = MOCK_STORES[pk]
        mock_obj = MockObject(store_data)
        
        has_perm, reason = PermissionChecker.check_permission(
            request.user, 'stores', 'delete', mock_obj
        )
        if not has_perm:
            return Response(
                {'error': reason}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        del MOCK_STORES[pk]
        return Response(status=status.HTTP_204_NO_CONTENT)


# ==================== USERS ENDPOINTS (Read-only mock) ====================

class UserListView(APIView):
    """
    GET /api/users/ - List users (filtered by permissions)
    """
    
    def get(self, request):
        """List users based on permissions"""
        result, error = check_list_permission(request, 'users', MOCK_USERS_DATA)
        if error:
            return error
        return Response(result, status=status.HTTP_200_OK)


class UserDetailView(APIView):
    """
    GET /api/users/{id}/ - Get single user
    """
    
    def get(self, request, pk):
        """Get single user"""
        if not request.user:
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if pk not in MOCK_USERS_DATA:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # For users endpoint, check read permission
        user_roles = request.user.user_roles.all().values_list('role', flat=True)
        
        try:
            element = BusinessElement.objects.get(name='users')
        except BusinessElement.DoesNotExist:
            return Response(
                {'error': 'Business element not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        rules = AccessRoleRule.objects.filter(role_id__in=user_roles, element=element)
        has_read = any(rule.read_all_permission or rule.read_permission for rule in rules)
        
        if not has_read:
            return Response(
                {'error': 'Insufficient permissions'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        return Response(MOCK_USERS_DATA[pk], status=status.HTTP_200_OK)
