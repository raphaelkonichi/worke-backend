# Generated by Django 4.1.2 on 2022-10-19 23:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=80)),
                ('cnpj', models.CharField(max_length=14)),
                ('email', models.CharField(max_length=50)),
                ('senha', models.CharField(max_length=50)),
                ('telefone', models.CharField(max_length=11)),
                ('data_criacao', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Exercicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=80)),
                ('categoria', models.CharField(choices=[], max_length=1)),
                ('data_criacao', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Expectativas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=50)),
                ('data_criacao', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=50)),
                ('codigo', models.CharField(max_length=4)),
                ('senha', models.CharField(max_length=50)),
                ('qtd_participantes', models.IntegerField()),
                ('data_criacao', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Plano',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('data_criacao', models.DateField()),
                ('valor', models.DecimalField(decimal_places=2, max_digits=3)),
                ('instrument', models.CharField(max_length=100)),
                ('max_participantes', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('sobrenome', models.CharField(max_length=80)),
                ('email', models.CharField(max_length=50)),
                ('senha', models.CharField(max_length=50)),
                ('cpf', models.CharField(max_length=11)),
                ('telefone', models.CharField(max_length=11)),
                ('genero', models.CharField(choices=[('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outros')], max_length=1)),
                ('data_nascimento', models.DateField()),
                ('data_criacao', models.DateField()),
                ('altura', models.IntegerField()),
                ('freq_exercicios', models.CharField(choices=[], max_length=1)),
                ('tipo_usuario', models.CharField(max_length=1)),
                ('pontuacao', models.IntegerField()),
                ('nivel', models.IntegerField()),
                ('imagem', models.BinaryField()),
                ('primeiro_acesso', models.BooleanField(default=False)),
                ('expectativas', models.ManyToManyField(to='workeApp.expectativas')),
                ('plano_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workeApp.plano')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario_grupo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pontuacao', models.IntegerField()),
                ('posicao_ranking', models.IntegerField()),
                ('data_criacao', models.DateField()),
                ('data_posicao', models.DateField()),
                ('grupo_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workeApp.grupo')),
                ('usuario_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workeApp.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Peso_usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_criacao', models.DateField()),
                ('data_medicao', models.DateField()),
                ('peso', models.DecimalField(decimal_places=2, max_digits=3)),
                ('usuario_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workeApp.usuario')),
            ],
        ),
        migrations.AddField(
            model_name='grupo',
            name='admin_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workeApp.usuario'),
        ),
        migrations.AddField(
            model_name='grupo',
            name='empresa_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workeApp.empresa'),
        ),
        migrations.CreateModel(
            name='Exercicio_usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_criacao', models.DateField()),
                ('favorito', models.BooleanField(default=False)),
                ('exercicio_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workeApp.exercicio')),
                ('usuario_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workeApp.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Exercicio_realizado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_criacao', models.DateField()),
                ('pontuacao', models.IntegerField()),
                ('duracao', models.IntegerField()),
                ('exercicio_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workeApp.exercicio')),
                ('usuario_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workeApp.usuario')),
            ],
        ),
        migrations.AddField(
            model_name='empresa',
            name='plano_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workeApp.plano'),
        ),
    ]
