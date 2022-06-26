# Generated by Django 2.0.1 on 2018-01-16 21:21

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
            name='SponsorInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_to', models.CharField(max_length=1000)),
                ('sponsor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sponsor_info', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]