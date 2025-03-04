# Generated by Django 4.2 on 2024-07-17 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Colleges', '0006_alter_university_crime_free_campus_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feestructure',
            name='hostel_fees',
            field=models.JSONField(default={'sem1': 1750, 'sem2': 1750, 'sem3': 0, 'sem4': 0, 'sem5': 0, 'sem6': 0}, null=True),
        ),
        migrations.AlterField(
            model_name='feestructure',
            name='one_time_charges',
            field=models.JSONField(default={'sem1': 1750, 'sem2': 1750, 'sem3': 0, 'sem4': 0, 'sem5': 0, 'sem6': 0}, null=True),
        ),
        migrations.AlterField(
            model_name='feestructure',
            name='totals',
            field=models.JSONField(default={'sem1': 1750, 'sem2': 1750, 'sem3': 0, 'sem4': 0, 'sem5': 0, 'sem6': 0}, null=True),
        ),
        migrations.AlterField(
            model_name='feestructure',
            name='tuition_fees',
            field=models.JSONField(default={'sem1': 1750, 'sem2': 1750, 'sem3': 0, 'sem4': 0, 'sem5': 0, 'sem6': 0}, null=True),
        ),
    ]
