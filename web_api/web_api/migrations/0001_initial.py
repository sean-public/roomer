# Generated by Django 2.0.3 on 2018-03-19 00:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Doorway',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='[optional] nickname for the device', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='DPU',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('active', models.BooleanField(default=True)),
                ('name', models.CharField(blank=True, help_text='[optional] nickname for the device', max_length=100)),
                ('doorway', models.ForeignKey(help_text='[optional] location where the device is installed', null=True, on_delete=django.db.models.deletion.SET_NULL, to='web_api.Doorway')),
            ],
        ),
        migrations.CreateModel(
            name='Occupancy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('count', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Space',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='occupancy',
            name='space',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_api.Space'),
        ),
        migrations.AddField(
            model_name='doorway',
            name='entering_to',
            field=models.ForeignKey(help_text='the space that this doorway enters into (and the sensor points into)', on_delete=django.db.models.deletion.PROTECT, related_name='doorway_entering_to', to='web_api.Space'),
        ),
        migrations.AddField(
            model_name='doorway',
            name='exiting_to',
            field=models.ForeignKey(help_text='the space that this doorway exits to (and is not visible to the sensor)', on_delete=django.db.models.deletion.PROTECT, related_name='doorway_exiting_to', to='web_api.Space'),
        ),
        migrations.AddIndex(
            model_name='occupancy',
            index=models.Index(fields=['space'], name='web_api_occ_space_i_a0ba15_idx'),
        ),
        migrations.AddIndex(
            model_name='occupancy',
            index=models.Index(fields=['timestamp'], name='web_api_occ_timesta_55dd9b_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='occupancy',
            unique_together={('space', 'timestamp')},
        ),
    ]