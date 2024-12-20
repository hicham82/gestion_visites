# Generated by Django 5.1.3 on 2024-11-13 16:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Personnel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('som_enseignant', models.CharField(max_length=20, unique=True)),
                ('cin_enseignant', models.CharField(max_length=20)),
                ('nom_enseignant', models.CharField(max_length=100)),
                ('cadre_enseignant', models.CharField(max_length=100)),
                ('date_affect_enseignant', models.DateField()),
                ('code_etab_enseignant', models.CharField(max_length=20)),
                ('etab_enseignant', models.CharField(max_length=100)),
                ('specialite_enseignant', models.CharField(max_length=100)),
                ('cycle_enseignant', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Visite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('som_inspecteur', models.CharField(max_length=20)),
                ('nom_inspecteur', models.CharField(max_length=100)),
                ('som_premier_accompagnateur', models.CharField(blank=True, max_length=20, null=True)),
                ('nom_premier_accompagnateur', models.CharField(blank=True, max_length=100, null=True)),
                ('etab_premier_accompagnateur', models.CharField(blank=True, max_length=100, null=True)),
                ('som_deuxieme_accompagnateur', models.CharField(blank=True, max_length=20, null=True)),
                ('nom_deuxieme_accompagnateur', models.CharField(blank=True, max_length=100, null=True)),
                ('etab_deuxieme_accompagnateur', models.CharField(blank=True, max_length=100, null=True)),
                ('date_visite', models.DateField()),
                ('heure_visite', models.TimeField()),
                ('centre_visite', models.CharField(max_length=100)),
                ('enseignant_visite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visites', to='inspections.personnel')),
            ],
        ),
    ]
