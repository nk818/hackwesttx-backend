from rest_framework import permissions

class IsStudentOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow students to create/edit content.
    Read permissions are allowed for any request.
    """
    def has_permission(self, request, view):
        # Read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only for authenticated students
        return request.user.is_authenticated and request.user.is_student()

class IsModeratorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow moderators to moderate content.
    Read permissions are allowed for any request.
    """
    def has_permission(self, request, view):
        # Read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only for moderators and admins
        return request.user.is_authenticated and request.user.can_moderate_content()

class IsAdminOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to access admin functions.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin()

class IsOwnerOrModerator(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or moderators to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only for the owner or moderators/admins
        if hasattr(obj, 'created_by'):
            return obj.created_by == request.user or request.user.can_moderate_content()
        elif hasattr(obj, 'user'):
            return obj.user == request.user or request.user.can_moderate_content()
        elif hasattr(obj, 'uploaded_by'):
            return obj.uploaded_by == request.user or request.user.can_moderate_content()
        
        return False

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only for the owner
        if hasattr(obj, 'created_by'):
            return obj.created_by == request.user
        elif hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'uploaded_by'):
            return obj.uploaded_by == request.user
        
        return False
