# Generated by Django 4.2.3 on 2023-08-01 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market_app', '0004_remove_listings_images_listings_image_1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='image_1',
            field=models.ImageField(blank=True, null=True, upload_to='listing_images/<autoslug.fields.AutoSlugField>/'),
        ),
    ]