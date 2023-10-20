from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement, Favorite  


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', 'draft' )
        read_only_fields = ['creator']

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        # TODO: добавьте требуемую валидацию
        if self.context["request"].method == 'POST':
            creator = self.context["request"].user
            count = Advertisement.objects.filter(creator=creator, status='OPEN').count()
            
            if count >= 10:
                raise ValidationError('Слишком много открытых объявлений!')

        return data
    

class FavoriteSerializer(serializers.ModelSerializer):
    advertisement = AdvertisementSerializer(
        read_only=True
    )

    class Meta:
        model = Favorite
        fields = ['advertisement', ]

    def create(self, validated_data):
        """Метод для создания"""
        validated_data['user'] = self.context['request'].user

        id = int(self.initial_data.get('advertisement'))
        validated_data['advertisement'] = Advertisement.objects.get(id=id)

        return super().create(validated_data)
    
    def validate(self, data):
        user = self.context['request'].user

        id = int(self.initial_data.get('advertisement'))
        advertisement = Advertisement.objects.get(id=id)

        if advertisement.creator == user:
            raise ValidationError('Свои объявления нельзя добавить в избранное!')
        
        if Favorite.objects.filter(user=user, advertisement=advertisement).exists():
            raise ValidationError('Нельзя добавить в избранное одно объявление два раза!')
        
        return data