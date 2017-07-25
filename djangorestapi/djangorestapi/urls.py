from django.conf.urls import url
from django.contrib import admin
from restapi.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import  include, url
from restapi.views import *
from rest_framework.authtoken import views

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

    url(r'^api/person_page_rank/$', ListCreatePersonPageRanks.as_view(), name = 'list_person_page_rank'),
    url(r'^api/person_page_rank/(?P<pk>\d+)', ListCreatePersonPageRank.as_view(), name = 'list_person_page_rank'),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^api/registration/', CreateUserView.as_view(), name = 'registration'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    #static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
