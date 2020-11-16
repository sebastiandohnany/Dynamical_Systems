# Generated by Django 3.1.1 on 2020-10-24 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='System',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='ParamA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a00', models.FloatField()),
                ('a01', models.FloatField()),
                ('a02', models.FloatField()),
                ('a10', models.FloatField()),
                ('a11', models.FloatField()),
                ('a12', models.FloatField()),
                ('a20', models.FloatField()),
                ('a21', models.FloatField()),
                ('a22', models.FloatField()),
                ('system', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visualisation.system')),
            ],
        ),
    ]