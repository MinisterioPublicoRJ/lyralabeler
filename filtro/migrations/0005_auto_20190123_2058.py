# Generated by Django 2.0.2 on 2019-01-23 20:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('filtro', '0004_itemfiltro_regex'),
    ]

    operations = [
        migrations.AddField(
            model_name='documento',
            name='classe_filtro',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='filtro.ClasseFiltro'),
        ),
        migrations.AlterField(
            model_name='documento',
            name='filtro',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='filtro.Filtro'),
            preserve_default=False,
        ),
    ]
