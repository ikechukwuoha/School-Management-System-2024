# Generated by Django 4.2.11 on 2024-04-05 16:07

from django.db import migrations
import shortuuid.django_fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_matricnumber_matric_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matricnumber',
            name='matric_number',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=6, max_length=5, prefix='IIC24', unique=True),
        ),
    ]
