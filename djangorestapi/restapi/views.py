from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from .serializers import *
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Q
import datetime
from .permission import *
# Create your views here.
from django.contrib.auth.hashers import  UnsaltedMD5PasswordHasher as md5

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


# Вносить сайты может только админ, пользователи лишь использовать
class ListCreateSites(generics.ListCreateAPIView):
    queryset = Sites.objects.all()
    serializer_class = SitesSerializers
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)

    def perform_create(self, serializer):
        serializer.save(UserID=self.request.user)

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            filter = Sites.objects.all()
        else:
            filter = Sites.objects.filter(UserID=self.request.user)
        return filter


# Изменять сайты может только админ, пользователи лишь смотреть
class ListCreateSite(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sites.objects.all()
    serializer_class = SitesSerializers
    permission_classes = (IsOwnerOrCloseOnlyForAdmin,)
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)

    def perform_create(self, serializer):
        serializer.save(UserID=self.request.user)

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
        if self.request.user.is_staff:
            filter = Persons.objects.all()
        else:
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
        if self.request.user.is_staff:
            filter = Keywords.objects.all()
        else:
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
    lookup_field = 'PersonID'

    def get_queryset(self, *args, **kwargs):

        filter = PersonPageRank.objects.filter(Q(PersonID = self.kwargs['pk'])|Q(PageID = self.kwargs['PageID']))
        return filter


class UserInfo(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserInfoSerializers
    permission_classes = (IsOwnerOrCloseOnlyForAdmin,)
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    lookup_field = 'username'

    def get_queryset(self, *args, **kwargs):
        filter = User.objects.filter(username = self.request.user)
        return filter


@api_view(['GET',])  
@permission_classes((IsAuthenticated, ))
def common_stat(request,site):
    data = {}
    pages = Pages.objects.filter(SiteID=site)
    if request.user.is_staff:
        persons = Persons.objects.all()
    else:
        try:
            persons = Persons.objects.filter(UserID=request.user)
        except:
            raise serializers.ValidationError('Требуется авторизация')
    if pages and persons:
        for person in persons:
            data[person.Name] = pages.filter(page_id__PersonID=person.pk)\
                                     .aggregate(Sum('page_id__Rank'))['page_id__Rank__sum'] or 0
        data['last_scan'] = pages.order_by('LastScanDate').last().LastScanDate
    else :
        return Response(status = status.HTTP_400_BAD_REQUEST)
    return Response(data)


@api_view(['GET',])
@permission_classes((IsAuthenticated, ))
def period_stat(request,site,person,date_from,date_to):
    data = {}
    pages = Pages.objects.filter(SiteID=site)
    person = get_object_or_404(Persons,pk=person)
    if person.UserID != request.user or not request.user.is_staff:
        return Response (status = status.HTTP_403_FORBIDDEN)
    if not pages:
        return Response (status = status.HTTP_400_BAD_REQUEST)
    pages_filtred = pages.filter(page_id__PersonID=person.pk).filter(FoundDateTime__range=(date_from,date_to))
    date = date_from.split('-')
    date = datetime.date(int(date[0]),int(date[1]),int(date[2]))
    date_to = date_to.split('-')
    date_to = datetime.date(int(date_to[0]),int(date_to[1]),int(date_to[2]))
    new_pages = 0
    while date != date_to:
        count = pages_filtred.filter(FoundDateTime__date=date).count()
        if count:
            data[date.isoformat()] = count
            new_pages +=count
        date += datetime.timedelta(days=1)
    data['new_pages'] = new_pages
    return Response(data)


'''@api_view(['GET',])
@permission_classes((IsAuthenticated, ))
def period_stat(request,site,person,date_from,date_to):
    data = {}
    pages = Pages.objects.filter(SiteID=site)
    if request.user.is_staff:
        person = get_object_or_404(Persons,pk=person)
    else:
        try:
            person = get_object_or_404(Persons, pk=person, UserID=request.user)
        except:
            raise serializers.ValidationError('Требуется авторизация')
    if not pages:
        return Response (status = status.HTTP_400_BAD_REQUEST)
    pages_filtred = pages.filter(page_id__PersonID=person.pk).filter(FoundDateTime__range=(date_from,date_to))
    date = date_from.split('-')
    date = datetime.date(int(date[0]),int(date[1]),int(date[2]))
    date_to = date_to.split('-')
    date_to = datetime.date(int(date_to[0]),int(date_to[1]),int(date_to[2]))
    new_pages = 0
    while date != date_to:
        count = pages_filtred.filter(FoundDateTime__date=date).count()
        if count:
            data[date.isoformat()] = count
            new_pages +=count
        date += datetime.timedelta(days=1)
    data['new_pages'] = new_pages
    return Response(data)'''
