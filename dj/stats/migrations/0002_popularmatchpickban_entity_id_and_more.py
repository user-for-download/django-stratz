# Generated by Django 4.2.11 on 2024-07-12 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='popularmatchpickban',
            name='entity_id',
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='popularmatchpickban',
            name='entity_type',
            field=models.CharField(choices=[('all', 'all'), ('league', 'league'), ('match', 'match'), ('player', 'player'), ('team', 'team')], default='all', max_length=10),
        ),
        migrations.AlterField(
            model_name='popularmatchpickban',
            name='time_stamp_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
