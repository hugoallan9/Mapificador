# Generated by Django 3.2.9 on 2021-11-17 02:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Mapificador', '0002_rename_excel_mapa_archivo_de_excel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mapa',
            old_name='archivo_de_excel',
            new_name='excel',
        ),
    ]
