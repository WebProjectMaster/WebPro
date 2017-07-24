from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
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

class CreateUserView(CreateAPIView):

    model = get_user_model()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer


class ListCreateSites(generics.ListCreateAPIView):
    queryset = Sites.objects.all()
    serializer_class = SitesSerializers
    permission_classes = (IsAuthenticated,)


class ListCreateSite(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sites.objects.all()
    serializer_class = SitesSerializers
    permission_classes = (IsAuthenticated,)

    def get_queryset(self,*args, **kwargs):
        filter = Sites.objects.filter(ID=self.kwargs['pk'])
        return filter


class ListCreatePages(generics.ListCreateAPIView):
    queryset = Pages.objects.all()
    serializer_class = PagesSerializers
    permission_classes = (IsAuthenticated,)


class ListCreatePage(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pages.objects.all()
    serializer_class = PagesSerializers
    permission_classes = (IsAuthenticated,)

    def get_queryset(self,*args, **kwargs):
        filter = Pages.objects.filter(ID=self.kwargs['pk'])
        return filter


class ListCreatePersons(generics.ListCreateAPIView):
    queryset = Persons.objects.all()
    serializer_class = PersonsSerializers
    permission_classes = (IsAuthenticated,)


class ListCreatePerson(generics.RetrieveUpdateDestroyAPIView):
    queryset = Persons.objects.all()
    serializer_class = PersonsSerializers
    permission_classes = (IsAuthenticated,)

    def get_queryset(self,*args, **kwargs):
        filter = Persons.objects.filter(ID=self.kwargs['pk'])
        return filter


class ListCreateKeywords(generics.ListCreateAPIView):
    queryset = Keywords.objects.all()
    serializer_class = KeywordsSerializers
    permission_classes = (IsAuthenticated,)


class ListCreateKeyword(generics.RetrieveUpdateDestroyAPIView):
    queryset = Keywords.objects.all()
    serializer_class = KeywordsSerializers
    permission_classes = (IsAuthenticated,)

    def get_queryset(self,*args, **kwargs):
        filter = Keywords.objects.filter(ID=self.kwargs['pk'])
        return filter


class ListCreatePersonPageRanks(generics.ListCreateAPIView):
    queryset = PersonPageRank.objects.all()
    serializer_class = PersonPageRankSerializers
    permission_classes = (IsAuthenticated,)


class ListCreatePersonPageRank(generics.RetrieveUpdateDestroyAPIView):
    queryset = PersonPageRank.objects.all()
    serializer_class = PersonPageRankSerializers
    permission_classes = (IsAuthenticated,)

    def get_queryset(self,*args, **kwargs):
        filter = PersonPageRank.objects.filter(ID=self.kwargs['pk'])
        return filter
