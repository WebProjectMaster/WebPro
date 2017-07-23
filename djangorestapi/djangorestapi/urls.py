"""djangorestapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from restapi.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import  include, url
from restapi.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^api/persons/$', ListCreatePersons.as_view(), name = 'list_persons'),
    url(r'^api/persons/(?P<pk>\d+)', ListCreatePerson.as_view(), name = 'list_persons'),

    url(r'^api/sites/$', ListCreateSites.as_view(), name = 'list_sites'),
    url(r'^api/sites/(?P<pk>\d+)', ListCreateSite.as_view(), name = 'list_sites'),

    url(r'^api/pages/$', ListCreatePages.as_view(), name = 'list_pages'),
    url(r'^api/pages', ListCreatePage.as_view(), name = 'list_pages'),

    url(r'^api/keywords/$', ListCreateKeywords.as_view(), name = 'list_keywords'),
    url(r'^api/keywords/(?P<pk>\d+)', ListCreateKeyword.as_view(), name = 'list_keywords'),

    url(r'^api/person_page_rank/$', ListCreatePersonPageRanks, name = 'list_person_page_rank'),
    url(r'^api/person_page_rank/(?P<pk>\d+)', ListCreatePersonPageRank, name = 'list_person_page_rank'),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    #static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
