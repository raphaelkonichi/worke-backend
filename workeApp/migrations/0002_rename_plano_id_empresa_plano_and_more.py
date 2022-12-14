# Generated by Django 4.1.2 on 2022-10-19 23:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workeApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='empresa',
            old_name='plano_id',
            new_name='plano',
        ),
        migrations.RenameField(
            model_name='exercicio_realizado',
            old_name='exercicio_id',
            new_name='exercicio',
        ),
        migrations.RenameField(
            model_name='exercicio_realizado',
            old_name='usuario_id',
            new_name='usuario',
        ),
        migrations.RenameField(
            model_name='exercicio_usuario',
            old_name='exercicio_id',
            new_name='exercicio',
        ),
        migrations.RenameField(
            model_name='exercicio_usuario',
            old_name='usuario_id',
            new_name='usuario',
        ),
        migrations.RenameField(
            model_name='grupo',
            old_name='admin_id',
            new_name='admin',
        ),
        migrations.RenameField(
            model_name='grupo',
            old_name='empresa_id',
            new_name='empresa',
        ),
        migrations.RenameField(
            model_name='peso_usuario',
            old_name='usuario_id',
            new_name='usuario',
        ),
        migrations.RenameField(
            model_name='usuario',
            old_name='plano_id',
            new_name='plano',
        ),
        migrations.RenameField(
            model_name='usuario_grupo',
            old_name='grupo_id',
            new_name='grupo',
        ),
        migrations.RenameField(
            model_name='usuario_grupo',
            old_name='usuario_id',
            new_name='usuario',
        ),
    ]
