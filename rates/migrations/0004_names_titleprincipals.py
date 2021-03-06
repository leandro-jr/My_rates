# Generated by Django 4.0.3 on 2022-04-06 18:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rates', '0003_titlebasics'),
    ]

    operations = [
        migrations.CreateModel(
            name='Names',
            fields=[
                ('nconst', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('primaryName', models.CharField(max_length=256)),
                ('birthYear', models.CharField(max_length=4)),
                ('deathYear', models.CharField(max_length=4)),
                ('primaryProfession', models.CharField(max_length=256)),
                ('knownForTitles', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='TitlePrincipals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordering', models.SmallIntegerField()),
                ('category', models.CharField(max_length=64)),
                ('job', models.CharField(max_length=64)),
                ('characters', models.CharField(max_length=256)),
                ('nconst', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='names_principals', to='rates.names')),
                ('tconst', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='titles_principals', to='rates.titlebasics')),
            ],
        ),
    ]
