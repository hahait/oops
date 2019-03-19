from rest_framework.permissions import DjangoModelPermissions

class MyDjangoModelPermissions(DjangoModelPermissions):

    def get_extra_perms(self,view,method):
        if hasattr(view,"extra_permission") and isinstance(view.extra_permission,dict):
            return view.extra_permission.get(method,[])
        return []

    def has_permission(self, request, view):
        if getattr(view, '_ignore_model_permissions', False):
            return True

        if not request.user or (
           not request.user.is_authenticated and self.authenticated_users_only):
            return False

        queryset = self._queryset(view)
        perms = self.get_required_permissions(request.method, queryset.model)
        perms.extend(self.get_extra_perms(view,request.method))
        print("perms: ",perms)
        return request.user.has_perms(perms)