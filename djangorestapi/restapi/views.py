from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from django.db.models import Q
from rest_framework.compat import is_authenticated
# Create your views here.
# Оставил лишнии импорты, мб пригодятся в разработке

'''
class ExampleView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        content = {
            'user': request.user,
            'auth': request.auth,
        }
        return Response(content)
'''


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


#сам лично писал, нужно оттестировать, ибо могут быть ошибки, ни где в инете гайда нету, кроме как офф. доки, так что могут быть ошибки, требует рефакторинга
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


class ListCreateSites(generics.ListCreateAPIView):
    queryset = Sites.objects.all()
    serializer_class = SitesSerializers
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)


class ListCreateSite(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sites.objects.all()
    serializer_class = SitesSerializers
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)

    def get_queryset(self,*args, **kwargs):
        filter = Sites.objects.filter(ID=self.kwargs['pk'])
        return filter


class ListCreatePages(generics.ListCreateAPIView):
    queryset = Pages.objects.all()
    serializer_class = PagesSerializers
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)


class ListCreatePage(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pages.objects.all()
    serializer_class = PagesSerializers
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)

    def get_queryset(self,*args, **kwargs):
        filter = Pages.objects.filter(ID=self.kwargs['pk'])
        return filter


class ListCreatePersons(generics.ListCreateAPIView):
    queryset = Persons.objects.all()
    serializer_class = PersonsSerializers
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)

    def perform_create(self, serializer):
        serializer.save(UserID=self.request.user)

    def get_queryset(self,*args, **kwargs):
        filter = Persons.objects.filter(UserID=self.request.user)
        return filter


class ListCreatePerson(generics.RetrieveUpdateDestroyAPIView):
    queryset = Persons.objects.all()
    serializer_class = PersonsSerializers
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)

    def get_queryset(self,*args, **kwargs):
        filter = Persons.objects.filter(ID=self.kwargs['pk'])
        return filter


class ListCreateKeywords(generics.ListCreateAPIView):
    queryset = Keywords.objects.all()
    serializer_class = KeywordsSerializers
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)

    def perform_create(self, serializer):
        serializer.save(UserID=self.request.user)

    def get_queryset(self,*args, **kwargs):
        filter = Keywords.objects.filter(UserID=self.request.user)
        return filter


class ListCreateKeyword(generics.RetrieveUpdateDestroyAPIView):
    queryset = Keywords.objects.all()
    serializer_class = KeywordsSerializers
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)

    def get_queryset(self,*args, **kwargs):
        filter = Keywords.objects.filter(ID=self.kwargs['pk'])
        return filter


class ListCreatePersonPageRanks(generics.ListCreateAPIView):
    queryset = PersonPageRank.objects.all()
    serializer_class = PersonPageRankSerializers
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)


class ListCreatePersonPageRank(generics.RetrieveUpdateDestroyAPIView):
    queryset = PersonPageRank.objects.all()
    serializer_class = PersonPageRankSerializers
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)

    def get_queryset(self,*args, **kwargs):
        filter = PersonPageRank.objects.filter(ID=self.kwargs['pk'])
        return filter


