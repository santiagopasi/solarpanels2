# Generated by Django 4.0.4 on 2022-06-22 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogApp', '0011_post_image_alter_post_tipo_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tipo_post',
            field=models.CharField(choices=[('Monocrystalline', 'Monocrystalline'), ('Polycrystalline', 'Polycrystalline')], max_length=40),
        ),
    ]
