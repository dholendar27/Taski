from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import mixins
from .models import Task
from .serializers import TaskSerializers
from rest_framework import status

class TaskView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin, GenericAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializers

    def post(self, request, *args, **kwargs):
        data = request.data
        title = data.get('title')
        description = data.get('description')
        status = data.get('status')
        
        if not title:
            return Response({"error": "Title is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        task = Task.objects.create(title=title, description=description, status=status)
        serialized_data = self.get_serializer(task)
        return Response(serialized_data.data, status=status.HTTP_201_CREATED)

    def get(self, request,pk = None, *args, **kwargs):
        tasks = ""
        if pk:
            tasks = self.get_queryset().filter(pk=pk).first()
            serialized_data = self.get_serializer(tasks, many=False)
        else:
            tasks = self.get_queryset()
            serialized_data = self.get_serializer(tasks, many=True)
        return Response(serialized_data.data, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        task = self.get_queryset().filter(pk=pk).first()
        
        if task:
            data = request.data
            task.title = data.get("title", task.title)
            task.description = data.get("description", task.description)
            task.status = data.get("status", task.status)
            task.save()
            
            serialized_data = self.get_serializer(task)
            return Response(serialized_data.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No Task found to update"}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk, *args, **kwargs):
        task = self.get_queryset().filter(pk=pk).first()
        
        if task:
            task.delete()
            return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "No Task found to delete"}, status=status.HTTP_404_NOT_FOUND)
