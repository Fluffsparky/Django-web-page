# Generated by Django 4.0.5 on 2023-03-04 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_rename_discription_listing_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='catagory',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='listing',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.URLField(blank=True, max_length=500),
        ),
    ]
