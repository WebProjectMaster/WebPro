""" Модели для WebPro"""


from django.db import models


class Sites(models.Model):
    """ Сайты """
    ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=256)


class Pages(models.Model):
    """ Страницы """
    ID = models.AutoField(primary_key=True)
    Url = models.URLField("url", max_length=2048)
    SiteID = models.ForeignKey(Sites, on_delete=models.CASCADE)
    FoundDateTime = models.DateTimeField("date found")
    LastScanDate = models.DateTimeField("last scan date")


class Persons(models.Model):
    """ Личности """
    ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=2048)


class Keywords(models.Model):
    """ Ключевые слова """
    ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=2048)
    PersonID = models.ForeignKey(Persons)


class PersonPageRank(models.Model):
    """ Ранг личностей на страницах """
    PersonID = models.ForeignKey(Persons)
    PageID = models.ForeignKey(Pages)
    Rank = models.IntegerField()
