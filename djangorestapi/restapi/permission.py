# сам лично писал, нужно оттестировать, ибо могут быть ошибки, ни где в инете гайда нету, кроме как офф. доки, так что могут быть ошибки, требует рефакторинга
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.compat import is_authenticated


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not is_authenticated(request.user):
           # print('Метод работает1')
            return False
        elif request.user.is_staff:
           # print('Метод работает2')
            return True
        elif request.method in permissions.SAFE_METHODS:
          #  print('Метод работает3')
            return True
        else:
          #  print('Метод работает4')
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        elif request.method in permissions.SAFE_METHODS:
            return request.user
        elif request.user.is_staff == False:
            return False
        else:
            return False


# Проверяет собственик записи человек или нет, если нет, доступа нет, если да, доступ есть,так же разрешён полный доступ админу
class IsOwnerOrCloseOnlyForAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            if obj.UserID:
                if obj.UserID == request.user:
                    return obj.UserID == request.user
                elif request.user.is_staff:
                    return True
                elif request.method in permissions.SAFE_METHODS:
                    return False
        except:
            if obj.username == request.user.username:
                return True
            else:
                return False
