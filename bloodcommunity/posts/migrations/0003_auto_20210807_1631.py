# Generated by Django 3.2.4 on 2021-08-07 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_ammount_blood'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='Ammount_blood',
        ),
        migrations.AddField(
            model_name='post',
            name='Ammount_of_blood',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')], default='1', max_length=10),
        ),
    ]
