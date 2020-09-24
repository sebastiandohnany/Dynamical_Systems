from django.db import models

class Matrix(models.Model):
    pass

class Parameter(models.Model):
    matrix = models.ForeignKey(Matrix, on_delete=models.CASCADE)
    row = models.IntegerField()
    col = models.IntegerField()
    a = models.FloatField()
