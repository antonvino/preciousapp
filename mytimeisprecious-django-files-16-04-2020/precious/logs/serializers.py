from django.forms import widgets
from rest_framework import serializers
from logs.models import Hour, Day, User
from registration.backends.default.views import RegistrationView


class HourSerializer(serializers.ModelSerializer):
    # author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Hour
        fields = ('id', 'day', 'hour', 'productive', 'hour_text', 'pub_date', 'author')


class DaySerializer(serializers.ModelSerializer):
    # author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Day
        fields = ('id', 'date', 'day_text', 'pub_date', 'author')

    # def validate(self, attrs):
    #     attrs = super(DaySerializer, self).validate(attrs)
    #
    #     year = attrs.get('year')
    #     month = attrs.get('month')
    #     day = attrs.get('day')
    #     author = attrs.get('author.id')
    #     # print json.dumps(attrs)
    #     print author
    #     author = User.objects.get(username=author)
    #
    #     try:
    #         obj = Day.objects.get(year=year, month=month, day=day, author=author)
    #     except Day.DoesNotExist:
    #         return attrs
    #     if self.object and obj.id == self.object.id:
    #         return attrs
    #     else:
    #         raise serializers.ValidationError('Not unique')


class UserSerializer(serializers.ModelSerializer):
    # days = serializers.PrimaryKeyRelatedField(many=True, queryset=Day.objects.all())
    # hours = serializers.PrimaryKeyRelatedField(many=True, queryset=Hour.objects.all())

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        # user.save()
        return user
