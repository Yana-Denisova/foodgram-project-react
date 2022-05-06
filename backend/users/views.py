from .models import Follow
from django.contrib.auth import get_user_model
from .serializers import FollowerListSerializer
from rest_framework import generics, permissions, views
from django.shortcuts import get_object_or_404

User = get_user_model()


class FollowerListView(generics.ListAPIView):
    """Вывод списка подписчиков"""
    permission_classes= [permissions.IsAuthenticated]
    serializer_class = FollowerListSerializer

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

class AddFollow(views.APIView):
    permission_classes= [permissions.IsAuthenticated]

    def post(self, request, id):

        author = get_object_or_404(User, pk=id)
        user = request.user
        if author != user:
            Follow.objects.get_or_create(user=user, author=author)
        return 