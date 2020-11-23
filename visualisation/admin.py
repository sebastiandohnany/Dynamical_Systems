from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.System)
admin.site.register(models.ParamA)
admin.site.register(models.ParamC)
admin.site.register(models.InitialValues)
admin.site.register(models.TimeSpan)
admin.site.register(models.Visible)
admin.site.register(models.IntegrationMaxStep)
admin.site.register(models.Description)