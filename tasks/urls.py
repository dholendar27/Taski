from django.urls import path
from . import views


urlpatterns = [
    path('',views.TaskView.as_view(),name='Task'),
    path('<int:pk>',views.TaskView.as_view(),name='Task'),
]