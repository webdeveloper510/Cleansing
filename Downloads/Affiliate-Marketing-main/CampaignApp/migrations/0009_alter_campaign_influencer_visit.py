# Generated by Django 4.1.7 on 2023-04-06 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CampaignApp', '0008_campaign_campaign_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='influencer_visit',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
