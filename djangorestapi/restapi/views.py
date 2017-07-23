from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *
# Create your views here.


class ListCreateSites(generics.ListCreateAPIView):
    queryset = Sites.objects.all()
    serializer_class = SitesSerializers


class ListCreatePages(generics.ListCreateAPIView):
    queryset = Pages.objects.all()
    serializer_class = PagesSerializers


class ListCreatePersons(generics.ListCreateAPIView):
    queryset = Persons.objects.all()
    serializer_class = KeywordsSerializers


class ListCreateKeywords(generics.ListCreateAPIView):
    queryset = Keywords.objects.all()
    serializer_class = KeywordsSerializers


class ListCreatePersonPageRank(generics.ListCreateAPIView):
    queryset = PersonPageRank.objects.all()
    serializer_class = PersonPageRankSerializers

