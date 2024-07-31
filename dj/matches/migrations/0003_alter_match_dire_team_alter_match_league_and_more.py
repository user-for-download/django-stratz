# Generated by Django 4.2.11 on 2024-07-11 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0001_initial'),
        ('teams', '0001_initial'),
        ('matches', '0002_alter_match_playback_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='dire_team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dire_matches', to='teams.team', to_field='id'),
        ),
        migrations.AlterField(
            model_name='match',
            name='league',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='matches', to='leagues.league', to_field='id'),
        ),
        migrations.AlterField(
            model_name='match',
            name='radiant_team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='radiant_matches', to='teams.team', to_field='id'),
        ),
        migrations.AlterField(
            model_name='match',
            name='series',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='matches', to='leagues.series', to_field='id'),
        ),
    ]
