import django_filters
from logs.models import Hour, Day, User
from logs.serializers import HourSerializer, DaySerializer, UserSerializer
from rest_framework import mixins, generics, filters, permissions
from logs.permissions import IsOwnerOrReadOnly, IsOwner, IsUser
from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

#  auth token specific
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import parsers
from rest_framework import renderers
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import status


from registration.backends.default.views import RegistrationView
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from registration import signals
from registration.models import RegistrationProfile

####
# Filters

class HourFilter(django_filters.FilterSet):
    synced_after = django_filters.DateTimeFilter(name="pub_date", lookup_type='gte')
    day = django_filters.Filter(name="day__id")

    class Meta:
        model = Hour
        fields = ['day', 'synced_after', 'hour']


class UserFilter(django_filters.FilterSet):

    class Meta:
        model = User
        fields = ['email', 'username']


class DayFilter(django_filters.FilterSet):
    synced_after = django_filters.DateTimeFilter(name="pub_date", lookup_type='gte')

    class Meta:
        model = Day
        fields = ['date', 'synced_after']


class HourList(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
    queryset = Hour.objects.all()
    serializer_class = HourSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = HourFilter
    permission_classes = (permissions.IsAuthenticated, IsOwner,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class HourDetail(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    queryset = Hour.objects.all()
    serializer_class = HourSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner,)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class DayList(mixins.ListModelMixin,
              mixins.CreateModelMixin,
              generics.GenericAPIView):
    queryset = Day.objects.all()
    serializer_class = DaySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = DayFilter
    permission_classes = (permissions.IsAuthenticated, IsOwner,)

    def get_queryset(self):
        """
        This view should return a list of all the days logged
        for the currently authenticated user.
        """
        # if self.request.user is not None:
        #     user = self.request.user
        #     return Day.objects.filter(author=user)
        # else:
        #     return Day.objects.all()
        return Day.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class DayDetail(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    queryset = Day.objects.all()
    serializer_class = DaySerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner,)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = UserFilter
    permission_classes = (permissions.IsAuthenticated,)
    from rest_framework.authtoken.models import Token
    for user in User.objects.all():
        Token.objects.get_or_create(user=user)


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsUser,)


class UserCreate(generics.CreateAPIView, RegistrationView):

    model = get_user_model()
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """
        Overriding perform_create() method of CreateAPIView
        Returns the instance created by the serializer
        """
        return serializer.save()

    def create(self, request, *args, **kwargs):
        """
        Overriding create() method of CreateAPIView
        Takes user_instance create by the serializer
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_user_instance = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # use the registration
        self.register(request=request, new_user_instance=new_user_instance)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def register(self, request, new_user_instance):
        """
        Overriding the method register() of RegistrationView
        Uses a user_instance already created by serializer

        """
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)

        new_user = RegistrationProfile.objects.create_inactive_user(
            new_user=new_user_instance,
            site=site,
            send_email=self.SEND_ACTIVATION_EMAIL,
            request=request,
        )
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user


class UserObtainAuthToken(ObtainAuthToken):

    renderer_classes = (JSONRenderer, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        data = {'token': token.key}
        return Response(data, status=status.HTTP_202_ACCEPTED)
