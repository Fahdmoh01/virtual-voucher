# Generated by Django 4.2.4 on 2023-08-20 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_eventvoucher_created_by"),
    ]

    operations = [
        migrations.AlterField(
            model_name="voucher",
            name="voucher_type",
            field=models.CharField(default="SILVER", max_length=50),
        ),
    ]