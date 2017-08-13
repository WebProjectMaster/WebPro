from rest_framework import serializers
from .models import Sites, Pages, Persons, Keywords, PersonPageRank
from django.contrib.auth import get_user_model
import hashlib

User = get_user_model()


# Регистрация обычного пользователя
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'password_confirm', 'email', 'email2', 'first_name', 'last_name',]
        write_only_fields = ('password', 'email2',)
        read_only_fields = ('id',)

    def validate_email(self, value):
        data = self.get_initial()
        email1 = data.get('email2')
        email2 = value
        if email1 != email2:
            raise serializers.ValidationError('Email не совпадают')
        user_email = User.objects.filter(email = email2)
        if user_email.exists():
            raise serializers.ValidationError('Данные имел уже зарегистрирован')

        return value

    email = serializers.EmailField(label ='Email адрес')
    email2 = serializers.EmailField(label ='Повторите Email адрес', write_only=True)

    password_confirm = serializers.CharField(label='Подтверждение пароля', style={'input_type': 'password'}, write_only=True)
    password = serializers.CharField(label='Пароль', style={'input_type': 'password'})

    def validate(self, validated_data):
        if validated_data['password'] != validated_data['password_confirm']:
            raise serializers.ValidationError('Пароли не совпадают!')

        return validated_data

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)
        validated_data.pop('email2', None)

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
        fields = ('id', 'username', 'password', 'password_confirm', 'email', 'email2', 'first_name', 'last_name', 'is_superuser', 'is_staff')
        write_only_fields = ('password', 'email2',)
        read_only_fields = ('id',)

    email = serializers.EmailField(label ='Email адрес')
    email2 = serializers.EmailField(label ='Повторите Email адрес', write_only=True)
    password_confirm = serializers.CharField(label='Подтверждение пароля', style={'input_type': 'password'}, write_only=True)
    password = serializers.CharField(label='Пароль', style={'input_type': 'password'})

    def validate(self, validated_data):
        if validated_data['password'] != validated_data['password_confirm']:
            raise serializers.ValidationError('Пароли не совпадают!')

        return validated_data


    def validate_email(self, value):
        data = self.get_initial()
        email1 = data.get('email2')
        email2 = value
        if email1 != email2:
            raise serializers.ValidationError('Email не совпадают')
        user_email = User.objects.filter(email = email2)
        if user_email.exists():
            raise serializers.ValidationError('Данные имел уже зарегистрирован')

        return value

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)
        validated_data.pop('email2', None)

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
    def __init__(self, *args, **kwargs):
        super(KeywordsSerializers, self).__init__(*args, **kwargs)
        self.fields['PersonID'].queryset = Persons.objects.filter(UserID=self.context['request'].user)

    class Meta:
        model = Keywords
        fields = ('ID', 'Name','PersonID')


# Ранг личностей на страницах
class PersonPageRankSerializers(serializers.ModelSerializer):
    class Meta:
        model = PersonPageRank
        fields = ('PersonID', 'PageID', 'Rank','Scan_date_datetime')


class UserInfoSerializers(serializers.ModelSerializer):
    old_password = serializers.CharField(label='Старый пароль', style={'input_type': 'password'},
                                             write_only=True)

    new_password = serializers.CharField(label='Новый пароль', style={'input_type': 'password'},
                                             write_only=True)

    password_confirm = serializers.CharField(label='Подтверждение пароля', style={'input_type': 'password'},
                                             write_only=True)

    def validate(self, validated_data):
        current_user = User.objects.get(username = self.context['request'].user)
        if hashlib.md5(validated_data['old_password'].encode("utf-8")).hexdigest() == current_user.password:
            if validated_data['new_password'] != validated_data['password_confirm']:
                raise serializers.ValidationError('Пароли не совпадают!')
        else:
            raise serializers.ValidationError(' Старый пароль не правильный ')
        return validated_data

    def update(self, instance, validated_data):
        current_user = User.objects.get(username=self.context['request'].user)
        current_user.set_password(validated_data['new_password'])
        current_user.save()
        return instance
    class Meta:
        model = User
        fields = ('id','username', 'first_name', 'last_name','old_password', 'new_password','password_confirm' )
        read_only_fields = ('id','username',)
