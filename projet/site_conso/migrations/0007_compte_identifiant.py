# Generated by Django 3.2.9 on 2021-12-16 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_conso', '0006_alter_compte_email_verifie'),
    ]

    operations = [
        migrations.AddField(
            model_name='compte',
            name='identifiant',
            field=models.IntegerField(null=True, unique=True),
        ),
    ]