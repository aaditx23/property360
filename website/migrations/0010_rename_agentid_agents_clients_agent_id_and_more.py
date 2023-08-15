# Generated by Django 4.2.2 on 2023-08-15 15:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_rename_agent_id_agents_clients_agentid_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='agents_clients',
            old_name='agentid',
            new_name='agent_id',
        ),
        migrations.RenameField(
            model_name='bids_in',
            old_name='auctionid',
            new_name='auction_id',
        ),
        migrations.RenameField(
            model_name='buyer',
            old_name='buyerid',
            new_name='buyer_id',
        ),
        migrations.RenameField(
            model_name='buys_from',
            old_name='agentid',
            new_name='agent_id',
        ),
        migrations.RenameField(
            model_name='dependent',
            old_name='agentid',
            new_name='agent_id',
        ),
        migrations.RenameField(
            model_name='maintains',
            old_name='supportid',
            new_name='support_id',
        ),
        migrations.RenameField(
            model_name='organizes',
            old_name='auctionid',
            new_name='auction_id',
        ),
        migrations.RenameField(
            model_name='property',
            old_name='agentid',
            new_name='agent_id',
        ),
        migrations.RenameField(
            model_name='property',
            old_name='propertyid',
            new_name='property_id',
        ),
        migrations.RenameField(
            model_name='property',
            old_name='userid',
            new_name='user_id',
        ),
        migrations.RenameField(
            model_name='seller',
            old_name='agentid',
            new_name='agent_id',
        ),
        migrations.AlterUniqueTogether(
            name='agents_clients',
            unique_together={('agent_id', 'client')},
        ),
        migrations.AlterUniqueTogether(
            name='bids_in',
            unique_together={('buyer_id', 'auction_id')},
        ),
        migrations.AlterUniqueTogether(
            name='buys_from',
            unique_together={('buyer_id', 'agent_id')},
        ),
        migrations.AlterUniqueTogether(
            name='maintains',
            unique_together={('property_id', 'support_id')},
        ),
        migrations.AlterUniqueTogether(
            name='organizes',
            unique_together={('admin_id', 'auction_id')},
        ),
        migrations.AlterUniqueTogether(
            name='seller',
            unique_together={('seller_id', 'agent_id')},
        ),
    ]
