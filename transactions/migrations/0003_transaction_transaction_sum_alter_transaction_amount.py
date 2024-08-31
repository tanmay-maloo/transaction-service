# Generated by Django 5.1 on 2024-08-31 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_rename_transacton_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='transaction_sum',
            field=models.FloatField(default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.FloatField(),
        ),
    ]
