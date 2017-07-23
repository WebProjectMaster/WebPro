from rest_framework import serializers
from .models import Sites, Pages, Persons, Keywords, PersonPageRank


# Сайты
class SitesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Sites
        fields = ('ID', 'Name')


# Страницы
class PagesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Pages
        fields = ('ID', 'Url', 'SiteID', 'FoundDateTime', 'LastScanDate')


# Личности
class PersonsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Persons
        fields = ('ID', 'Name')


# Ключевые слова
class KeywordsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Keywords
        fields = ('ID', 'Name', 'PersonID')


# Ранг личностей на страницах
class PersonPageRankSerializers(serializers.ModelSerializer):
    class Meta:
        model = PersonPageRank
        fields = ('PersonID', 'PageID', 'Rank')
