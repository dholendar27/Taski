from django.db import models

# Create your models here.
TASKS_STATUS = (('1','Not started'),('2','Started'),('3','Completed'))


class Task(models.Model):
    title = models.CharField(max_length=100, unique=True,null=False,blank=False)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=TASKS_STATUS, default='1')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title