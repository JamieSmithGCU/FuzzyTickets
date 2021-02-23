# Generated by Django 3.1.2 on 2021-02-23 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_item_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='venue',
            field=models.CharField(choices=[('SECC', 'Scottish Exhibition & Conference Centre'), ('KT', 'King Tuts Wah Wah Hut'), ('BB', 'Barrowland Ballroom'), ('HP', 'Hampden Park')], max_length=10),
        ),
    ]
