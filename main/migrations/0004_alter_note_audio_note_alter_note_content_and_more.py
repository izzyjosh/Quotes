# Generated by Django 5.0 on 2024-01-31 17:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0003_alter_noteshared_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="note",
            name="audio_note",
            field=models.FileField(blank=True, null=True, upload_to="audio_note"),
        ),
        migrations.AlterField(
            model_name="note",
            name="content",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="note",
            name="video_note",
            field=models.FileField(blank=True, null=True, upload_to="video_note"),
        ),
    ]
