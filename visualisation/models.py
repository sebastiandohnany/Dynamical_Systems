from django.db import models


class System(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name


class ParamA(models.Model):
    a00 = models.FloatField(default=0)
    a01 = models.FloatField(default=0)
    a02 = models.FloatField(default=0)
    a03 = models.FloatField(default=0)
    a04 = models.FloatField(default=0)

    a10 = models.FloatField(default=0)
    a11 = models.FloatField(default=0)
    a12 = models.FloatField(default=0)
    a13 = models.FloatField(default=0)
    a14 = models.FloatField(default=0)

    a20 = models.FloatField(default=0)
    a21 = models.FloatField(default=0)
    a22 = models.FloatField(default=0)
    a23 = models.FloatField(default=0)
    a24 = models.FloatField(default=0)

    a30 = models.FloatField(default=0)
    a31 = models.FloatField(default=0)
    a32 = models.FloatField(default=0)
    a33 = models.FloatField(default=0)
    a34 = models.FloatField(default=0)

    a40 = models.FloatField(default=0)
    a41 = models.FloatField(default=0)
    a42 = models.FloatField(default=0)
    a43 = models.FloatField(default=0)
    a44 = models.FloatField(default=0)

    system = models.OneToOneField(System, on_delete=models.CASCADE)


class ParamC(models.Model):
    c0 = models.FloatField(default=0)
    c1 = models.FloatField(default=0)
    c2 = models.FloatField(default=0)
    c3 = models.FloatField(default=0)
    c4 = models.FloatField(default=0)

    system = models.OneToOneField(System, on_delete=models.CASCADE)


class InitialValues(models.Model):
    x0 = models.FloatField(default=0)
    x1 = models.FloatField(default=0)
    x2 = models.FloatField(default=0)
    x3 = models.FloatField(default=0)
    x4 = models.FloatField(default=0)

    system = models.OneToOneField(System, on_delete=models.CASCADE)


class TimeSpan(models.Model):
    start = models.FloatField(default=0)
    end = models.FloatField(default=0)

    system = models.OneToOneField(System, on_delete=models.CASCADE)


class Visible(models.Model):
    x0 = models.BooleanField(default=True)
    x1 = models.BooleanField(default=True)
    x2 = models.BooleanField(default=False)
    x3 = models.BooleanField(default=False)
    x4 = models.BooleanField(default=False)

    system = models.OneToOneField(System, on_delete=models.CASCADE)


class IntegrationMaxStep(models.Model):
    step = models.FloatField(default=0.1)

    system = models.OneToOneField(System, on_delete=models.CASCADE)
