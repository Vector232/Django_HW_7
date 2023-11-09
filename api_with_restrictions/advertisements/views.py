from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import Advertisement, Favorite
from .serializers import AdvertisementSerializer, FavoriteSerializer
from .permissions import IsOwner
from .filters import AdvertisementFilter, FavoriteFilter



class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
        
    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров
    def get_queryset(self):
        queryset = Advertisement.objects.filter(draft=False).all()

        current_user = self.request.user
        current_user_authorization = self.request.user.is_authenticated

        if current_user_authorization:
            queryset_draft = Advertisement.objects.filter(draft=True, creator=current_user).all()
            return queryset | queryset_draft
        return queryset

    
    serializer_class = AdvertisementSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AdvertisementFilter


class FavoriteViewSet(ModelViewSet):
    """ViewSet для избранного."""
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsOwner]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = FavoriteFilter
