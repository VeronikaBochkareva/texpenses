from django.db import models


class Users(models.Model):
    name = models.CharField(max_length=30)
    limit = models.IntegerField()


class Categories(models.Model):
    name = models.CharField(max_length=30)
    users = models.ManyToManyField(Users, through="Settings")


class Settings(models.Model):
    users = models.ForeignKey(Categories, on_delete=models.CASCADE)
    categories = models.ForeignKey(Users, on_delete=models.CASCADE)
    total = models.IntegerField()
