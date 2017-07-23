""" Модели для WebPro"""


from django.db import models


class Sites(models.Model):
    """ Сайты """

    class Meta:
        db_table = "sites"

    ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=256)


class Pages(models.Model):
    """ Страницы """

    class Meta:
        db_table = "pages"

    ID = models.AutoField(primary_key=True)
    Url = models.URLField("url", max_length=2048)
    SiteID = models.ForeignKey(Sites, db_column="SiteID")
    FoundDateTime = models.DateTimeField("date found")
    LastScanDate = models.DateTimeField("last scan date")


class Persons(models.Model):
    """ Личности """

    class Meta:
        db_table = "persons"

    ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=2048)


class Keywords(models.Model):
    """ Ключевые слова """

    class Meta:
        db_table = "keywords"

    ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=2048)
    PersonID = models.ForeignKey(Persons, db_column="PersonID")


class PersonPageRank(models.Model):
    """ Ранг личностей на страницах """

    class Meta:
        db_table = "person_page_rank"

    PersonID = models.ForeignKey(Persons, db_column="PersonID")
    PageID = models.ForeignKey(Pages, db_column="PageID")
    Rank = models.IntegerField()
