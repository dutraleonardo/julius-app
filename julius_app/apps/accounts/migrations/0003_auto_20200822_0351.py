# Generated by Django 2.2.11 on 2020-08-22 03:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200819_0350'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(blank=True, choices=[('adicionar', 'adicionar'), ('remover', 'remover')], max_length=124, null=True, verbose_name='transaction_type'),
        ),
        migrations.AlterField(
            model_name='card',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='card', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AlterField(
            model_name='user',
            name='account_type',
            field=models.CharField(blank=True, choices=[('company', 'company'), ('person', 'person')], max_length=124, null=True, verbose_name='account_type'),
        ),
    ]
