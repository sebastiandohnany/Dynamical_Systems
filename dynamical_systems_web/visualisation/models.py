from django.db import models


class System(models.Model):
    name = models.CharField(max_length=80)


class ParamA(models.Model):
    a00 = models.FloatField()
    a01 = models.FloatField()
    a02 = models.FloatField()

    a10 = models.FloatField()
    a11 = models.FloatField()
    a12 = models.FloatField()

    a20 = models.FloatField()
    a21 = models.FloatField()
    a22 = models.FloatField()

    system = models.ForeignKey(System, on_delete=models.CASCADE)
