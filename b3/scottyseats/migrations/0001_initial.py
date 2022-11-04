# Generated by Django 4.1.2 on 2022-10-09 01:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BoardModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fruittilelist', models.TextField()),
                ('gameongoing', models.BooleanField()),
                ('createdtime', models.FloatField()),
                ('roomnumber', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(max_length=200)),
                ('update_time', models.DateTimeField()),
                ('picture', models.FileField(blank=True, upload_to='')),
                ('content_type', models.CharField(max_length=50)),
                ('following', models.ManyToManyField(related_name='followers', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PlayerModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=10)),
                ('tilelist', models.TextField()),
                ('lastdirection', models.CharField(max_length=5)),
                ('snakelength', models.IntegerField()),
                ('isplaying', models.BooleanField(default=False)),
                ('color', models.IntegerField()),
                ('starttime', models.FloatField()),
                ('lastmovetime', models.FloatField()),
                ('movesmade', models.IntegerField()),
                ('lasttail', models.IntegerField()),
                ('roomnumber', models.IntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='playerone', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CommentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=200)),
                ('update_time', models.DateTimeField()),
                ('commented_post_id', models.IntegerField()),
                ('post_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='comment_creators', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
