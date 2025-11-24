from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Achievement, Cat

from .serializers import AchievementSerializer, CatSerializer


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    pagination_class = PageNumberPagination 

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    def get_serializer_context(self):
        """Передаем request в контекст сериализатора для построения полных URL"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context 


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    pagination_class = None