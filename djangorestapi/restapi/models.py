""" Модели для WebPro"""
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
class Sites(models.Model):
    """ Сайты """

    class Meta:
        db_table = "sites"

    ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=256)

    def __str__(self):
        return self.Name


class Pages(models.Model):
    """ Страницы """

    class Meta:
        db_table = "pages"


    ID = models.AutoField(primary_key=True)
    Url = models.URLField("url", max_length=128)
    Hash_url = models.URLField("url", unique=True, max_length=32)
    SiteID = models.ForeignKey(Sites, db_column="SiteID")
    FoundDateTime = models.DateTimeField("date found")
    LastScanDate = models.DateTimeField("last scan date", null=True, blank=True)

    def __str__(self):
        return self.Url

class Persons(models.Model):
    """ Личности """

    class Meta:
        db_table = "persons"

    ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=2048)
    UserID = models.ForeignKey(User, db_column="username", blank=True)


    def __str__(self):
        return self.Name


class Keywords(models.Model):
    """ Ключевые слова """

    class Meta:
        db_table = "keywords"

    ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=2048)
    PersonID = models.ForeignKey(Persons,limit_choices_to={'username': 'UserID'}, db_column="PersonID")
    UserID = models.ForeignKey(User, db_column="username", blank=True, )

    def __str__(self):
        return self.Name


class PersonPageRank(models.Model):
    """ Ранг личностей на страницах """

    class Meta:
        db_table = "person_page_rank"

    PersonID = models.ForeignKey(Persons, db_column="PersonID")
    PageID = models.ForeignKey(Pages, db_column="PageID")
    Rank = models.IntegerField()
    Scan_date_datetime = models.DateTimeField("Scan Date Datetime", null=True, blank=True)

    def __str__(self):
        return self.PersonID
