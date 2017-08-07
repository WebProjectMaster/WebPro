from rest_framework import serializers
from .models import Sites, Pages, Persons, Keywords, PersonPageRank
from django.contrib.auth import get_user_model

User = get_user_model()


# Регистрация обычного пользователя
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'password_confirm', 'email', 'first_name', 'last_name',)
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    password_confirm = serializers.CharField(label='Подтверждение пароля', style={'input_type': 'password'}, write_only=True)
    password = serializers.CharField(label='Пароль', style={'input_type': 'password'})

    def validate(self, validated_data):
        if validated_data['password'] != validated_data['password_confirm']:
            raise serializers.ValidationError('Пароли не совпадают!')

        return validated_data

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)

        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


# Регистрация администратора
class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'password_confirm', 'email', 'first_name', 'last_name', 'is_superuser', 'is_staff')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    password_confirm = serializers.CharField(label='Подтверждение пароля', style={'input_type': 'password'}, write_only=True)
    password = serializers.CharField(label='Пароль', style={'input_type': 'password'})

    def validate(self, validated_data):
        if validated_data['password'] != validated_data['password_confirm']:
            raise serializers.ValidationError('Пароли не совпадают!')

        return validated_data

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)

        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_superuser=validated_data['is_superuser'],
            is_staff=validated_data['is_staff'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


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
        fields = ('ID', 'Name','PersonID')


# Ранг личностей на страницах
class PersonPageRankSerializers(serializers.ModelSerializer):
    class Meta:
        model = PersonPageRank
        fields = ('PersonID', 'PageID', 'Rank','Scan_date_datetime')



