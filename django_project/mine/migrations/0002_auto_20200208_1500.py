# Generated by Django 2.2.9 on 2020-02-08 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mine', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'verbose_name': '购物车', 'verbose_name_plural': '购物车'},
        ),
        migrations.AlterModelOptions(
            name='comments',
            options={'ordering': ['-reorder'], 'verbose_name': '商品评价', 'verbose_name_plural': '商品评价'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': '订单', 'verbose_name_plural': '订单'},
        ),
    ]