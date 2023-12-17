# Generated by Django 4.2.5 on 2023-12-16 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0040_order_payment_method'),
    ]

    operations = [
        migrations.CreateModel(
            name='VoucherCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vouchercode', models.CharField(max_length=200)),
                ('voucher_percentage', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=5)),
                ('final_amount', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10)),
            ],
        ),
        migrations.RemoveField(
            model_name='item',
            name='discount_name',
        ),
        migrations.RemoveField(
            model_name='order',
            name='payment_method',
        ),
        migrations.AddField(
            model_name='order',
            name='category',
            field=models.ManyToManyField(blank=True, default='Not available', null=True, to='projects.vouchercode'),
        ),
    ]
