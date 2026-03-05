from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Todo
from .serializer import TodoSerializer, TodoCreateUpdateSerializer


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.filter(deleted_at__isnull=True)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_done', 'priority']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'due_date', 'priority']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TodoCreateUpdateSerializer
        return TodoSerializer

    def perform_destroy(self, instance):
        instance.soft_delete()

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        todo = self.get_object()
        todo.is_done = True
        todo.save()
        serializer = self.get_serializer(todo)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def uncomplete(self, request, pk=None):
        todo = self.get_object()
        todo.is_done = False
        todo.save()
        serializer = self.get_serializer(todo)
        return Response(serializer.data)
