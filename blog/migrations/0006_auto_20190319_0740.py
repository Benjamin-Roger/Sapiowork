# Generated by Django 2.1.7 on 2019-03-19 07:40

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20190319_0247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='body_stream',
            field=wagtail.core.fields.StreamField([('heading', wagtail.core.blocks.RichTextBlock()), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())], blank=True),
        ),
        migrations.AlterField(
            model_name='blogpage',
            name='body_stream_en',
            field=wagtail.core.fields.StreamField([('heading', wagtail.core.blocks.RichTextBlock()), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='blogpage',
            name='body_stream_fr',
            field=wagtail.core.fields.StreamField([('heading', wagtail.core.blocks.RichTextBlock()), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())], blank=True, null=True),
        ),
    ]
