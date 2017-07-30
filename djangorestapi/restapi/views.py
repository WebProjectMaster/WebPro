from rest_framework import generics
from .serializers import *
from django.conf import settings
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import permissions
from django.db.models import Q
from rest_framework.compat import is_authenticated
# Create your views here.


# Регистрация обычного пользователя
class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer


# Регистрация администратора
class AdminRegistration(CreateAPIView):
    model = get_user_model()
    permission_classes = [
        permissions.IsAdminUser
    ]
    serializer_class = AdminSerializer


# сам лично писал, нужно оттестировать, ибо могут быть ошибки, ни где в инете гайда нету, кроме как офф. доки, так что могут быть ошибки, требует рефакторинга
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not is_authenticated(request.user):
            print('Метод работает1')
            return False
        elif request.user.is_staff:
            print('Метод работает2')
            return True
        elif request.method in permissions.SAFE_METHODS:
            print('Метод работает3')
            return True
        else:
            print('Метод работает4')
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
        if obj.UserID == request.user:
            return obj.UserID == request.user
        elif request.user.is_staff:
            return True
        elif request.method in permissions.SAFE_METHODS:
            return False



# Вносить сайты может только админ, пользователи лишь использовать
class ListCreateSites(generics.ListCreateAPIView):
    queryset = Sites.objects.all()
    serializer_class = SitesSerializers
    permission_classes = (IsAdminOrReadOnly,)
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)


# Изменять сайты может только админ, пользователи лишь смотреть
class ListCreateSite(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sites.objects.all()
    serializer_class = SitesSerializers
    permission_classes = (IsAdminOrReadOnly,)
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)

    def get_queryset(self, *args, **kwargs):
        filter = Sites.objects.filter(ID=self.kwargs['pk'])
        return filter


# заполняется краулером, доступно только админу
class ListCreatePages(generics.ListCreateAPIView):
    queryset = Pages.objects.all()
    serializer_class = PagesSerializers
    permission_classes = (IsAdminUser,)
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)


# заполняется краулером, доступно только админу
class ListCreatePage(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pages.objects.all()
    serializer_class = PagesSerializers
    permission_classes = (IsAdminUser,)
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)

    def get_queryset(self, *args, **kwargs):
        filter = Pages.objects.filter(ID=self.kwargs['pk'])
        return filter


# Доступ по аутентификация и фильтрация по юзеру
class ListCreatePersons(generics.ListCreateAPIView):
    queryset = Persons.objects.all()
    serializer_class = PersonsSerializers
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)

    def perform_create(self, serializer):
        serializer.save(UserID=self.request.user)

    def get_queryset(self, *args, **kwargs):
        filter = Persons.objects.filter(UserID=self.request.user)
        return filter


# Доступ только собственику записи или админу
class ListCreatePerson(generics.RetrieveUpdateDestroyAPIView):
    queryset = Persons.objects.all()
    serializer_class = PersonsSerializers
    permission_classes = (IsOwnerOrCloseOnlyForAdmin,)
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)

    def perform_create(self, serializer):
        serializer.save(UserID=self.request.user)

    def get_queryset(self, *args, **kwargs):
        filter = Persons.objects.filter(ID=self.kwargs['pk'])
        return filter


# Доступ по аутентификация и фильтрация по юзеру
class ListCreateKeywords(generics.ListCreateAPIView):
    queryset = Keywords.objects.all()
    serializer_class = KeywordsSerializers
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)

    def perform_create(self, serializer):
        serializer.save(UserID=self.request.user)

    def get_queryset(self, *args, **kwargs):

        filter = Keywords.objects.filter(UserID=self.request.user)
        return filter


# Доступ только собственику записи или админу
class ListCreateKeyword(generics.RetrieveUpdateDestroyAPIView):
    queryset = Keywords.objects.all()
    serializer_class = KeywordsSerializers
    permission_classes = (IsOwnerOrCloseOnlyForAdmin,)
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)

    def get_queryset(self, *args, **kwargs):
        filter = Keywords.objects.filter(ID=self.kwargs['pk'])
        return filter


# Изменяется краулром доступно только админу
class ListCreatePersonPageRanks(generics.ListCreateAPIView):
    queryset = PersonPageRank.objects.all()
    serializer_class = PersonPageRankSerializers
    permission_classes = (IsAdminUser,)
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)


# Изменяется краулром доступно только админу
class ListCreatePersonPageRank(generics.RetrieveUpdateDestroyAPIView):
    queryset = PersonPageRank.objects.all()
    serializer_class = PersonPageRankSerializers
    permission_classes = (IsAdminUser,)
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)

    def get_queryset(self, *args, **kwargs):
        filter = PersonPageRank.objects.filter(ID=self.kwargs['pk'])
        return filter
