# Generated by Django 5.1 on 2024-08-29 12:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cli', '0007_create_default_commands'),
    ]

    operations = [
        migrations.AlterField(
            model_name='command',
            name='url',
            field=models.URLField(blank=True, help_text='The command is redirected to this URL. <code>%s</code> in the URL is replaced with the command argument.'),
        ),
        migrations.CreateModel(
            name='Override',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('argument', models.CharField(blank=True, max_length=32)),
                ('title', models.CharField(max_length=64)),
                ('url', models.URLField(help_text='The command is redirected to this URL. <code>%s</code> in the URL is replaced with the command argument.')),
                ('command', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='overrides', to='cli.command')),
            ],
        ),
    ]
