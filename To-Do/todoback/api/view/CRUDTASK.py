import datetime
from rest_framework import viewsets, permissions,status
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models import Task
from ..serializers import TaskSerializer, TaskStatusUpdateSerializer

"""
| Method | Endpoint                  | Description        |
| ------ | ------------------------- | ------------------ |
| GET    | `/api/tasks/`             | List all tasks     |
| POST   | `/api/tasks/`             | Create a new task  |
| GET    | `/api/tasks/{id}/`        | Retrieve a task    |
| PUT    | `/api/tasks/{id}/`        | Update a task      |
| PATCH  | `/api/tasks/{id}/`        | Partial update     |
| DELETE | `/api/tasks/{id}/`        | Delete a task      |
| PATCH  | `/api/tasks/{id}/status/` | Update task status |
"""


class TaskCRUD(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = self.request.data
        data['personid'] = self.request.user.id
        deadline = data.get('deadline')
        if deadline < str(datetime.datetime.now()):
            data['status'] = "PASSED"
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def list(self, request, *args, **kwargs):
        personid = self.request.user.id
        tasks = Task.objects.filter(personid=personid)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], url_path='status')
    def update_status(self, request, pk=None):
        task = self.get_object()
        serializer = TaskStatusUpdateSerializer(
            task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
