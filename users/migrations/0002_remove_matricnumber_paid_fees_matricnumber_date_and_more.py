# Generated by Django 4.2.11 on 2024-04-05 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='matricnumber',
            name='paid_fees',
        ),
        migrations.AddField(
            model_name='matricnumber',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='matricnumber',
            name='student_status',
            field=models.CharField(choices=[('active', 'Active'), ('in-active', 'In-Active')], default='in-active', max_length=100),
        ),
    ]
