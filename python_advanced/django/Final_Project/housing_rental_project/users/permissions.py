from rest_framework import permissions


class IsLandlord(permissions.BasePermission):
    """Custom permission that gives access only to the Landlord group users"""
    message = 'Access allowed only for Landlords'

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        #checking if user belongs to Landlord group
        return request.user.groups.filter(name='Landlords').exists()
    

class IsOwnerOrReadOnly(permissions.BasePermission):
    """Custom permission that allows owner to edit\delete ad, and for others only view it"""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.owner == request.user