from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *
# Create your views here.


class ListCreateSites(generics.ListCreateAPIView):
    queryset = Sites.objects.all()
    serializer_class = SitesSerializers

class ListCreateSite(ListCreateSites):
    def get_queryset(self,*args, **kwargs):
        filter = Sites.objects.filter(ID=self.kwargs['pk'])
        return filter


class ListCreatePages(generics.ListCreateAPIView):
    queryset = Pages.objects.all()
    serializer_class = PagesSerializers


class ListCreatePage(ListCreatePages):
    def get_queryset(self,*args, **kwargs):
        filter = Pages.objects.filter(ID=self.kwargs['pk'])
        return filter


class ListCreatePersons(generics.ListCreateAPIView):
    queryset = Persons.objects.all()
    serializer_class = PersonsSerializers


class ListCreatePerson(ListCreatePersons):
    def get_queryset(self,*args, **kwargs):
        filter = Persons.objects.filter(ID=self.kwargs['pk'])
        return filter


class ListCreateKeywords(generics.ListCreateAPIView):
    queryset = Keywords.objects.all()
    serializer_class = KeywordsSerializers


class ListCreateKeyword(ListCreateKeywords):
    def get_queryset(self,*args, **kwargs):
        filter = Keywords.objects.filter(ID=self.kwargs['pk'])
        return filter


class ListCreatePersonPageRanks(generics.ListCreateAPIView):
    queryset = PersonPageRank.objects.all()
    serializer_class = PersonPageRankSerializers


class ListCreatePersonPageRank(ListCreatePersonPageRanks):
    def get_queryset(self,*args, **kwargs):
        filter = PersonPageRank.objects.filter(ID=self.kwargs['pk'])
        return filter
