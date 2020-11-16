# Generated by Django 2.2.10 on 2020-10-24 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='attached_products',
        ),
        migrations.AddField(
            model_name='good',
            name='attached_products',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='article', to='shop.Article'),
        ),
    ]