# Generated by Django 4.1.3 on 2023-01-31 21:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workeApp', '0008_alter_usuario_tipo_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='data_ultimo_acesso',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
