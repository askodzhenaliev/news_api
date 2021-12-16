from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from .permissions import IsPostAuthor

from .models import Post, Comment
from .serializers import *


class IsAuthorPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user == obj.author


class PermissionMixin:
    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsAuthenticated, ]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthorPermission, ]
        else:
            permissions = []
        return [permission() for permission in permissions]


class CommentViewSet(PermissionMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, ]

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsPostAuthor, ]
        else:
            permissions = [IsAuthenticated, ]
        return [permission() for permission in permissions]

    @action(detail=False, methods=['get'])
    def search(self, request, pk=None):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(title__icontains=q) |
                                   Q(text__icontains=q))
        serializer = PostSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)



