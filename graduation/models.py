from django.db import models

# Create your models here.
from django.conf import settings


class User(models.Model):
    username = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=13)
    email = models.EmailField()

    def __str__(self):
        return u'{} {} '.format(self.first_name, self.last_name)


class Teacher(User):
    t_num = models.IntegerField(max_length=10)
    degree = models.CharField(max_length=150)

    def __str__(self):
        return u'{} {} '.format(self.first_name, self.last_name)


class Student(User):
    st_num = models.IntegerField(max_length=10)
    level = models.IntegerField(max_length=1)

    def __str__(self):
        return u'{} {} '.format(self.first_name, self.last_name)


class Project(models.Model):
    project_title = models.CharField(max_length=150)
    project_degree = models.IntegerField(max_length=1)
    group_members = models.ManyToManyField(to=Student)
    project_supervisor = models.ManyToManyField(to=Teacher)
    project_description = models.TextField(max_length=10000)
    status_selection = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected')
    ]
    status = models.CharField(max_length=9, choices=status_selection, default='Pending')

    def __str__(self):
        return self.project_title

    def getGroupeMembers(self):
        return self.group_members


class Meeting(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    project_supervisor = models.ManyToManyField(to=Teacher)
    date = models.CharField(max_length=100, null=True, blank=True)
    status_selection = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected')
    ]
    status = models.CharField(max_length=9, choices=status_selection, default='Pending')

    def __str__(self):
        return self.project.project_title

class ProgressReport(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    project_supervisor = models.ManyToManyField(to=Teacher)
    date = models.DateTimeField(auto_now_add=True)
    teacher_replay = models.TextField(null=True, blank=True)
    report = models.FileField(upload_to='documents/%Y/%m/%d')

    def __str__(self):
        return self.project.project_title