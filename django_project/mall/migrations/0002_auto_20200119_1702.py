# Generated by Django 2.2.9 on 2020-01-19 17:02

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('mall', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classify',
            name='uid',
            field=models.UUIDField(default=uuid.UUID('8414f8de-ec4a-4793-8ad0-364b071de761'), editable=False, verbose_name='分类ID'),
        ),
        migrations.AlterField(
            model_name='product',
            name='uid',
            field=models.UUIDField(default=uuid.UUID('4ca102a4-5608-4fff-bd86-31927111ebae'), editable=False, verbose_name='商品id'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='uid',
            field=models.UUIDField(default=uuid.UUID('7e804a57-e657-439b-9b34-93c8b1eda070'), editable=False, verbose_name='分类ID'),
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('reorder', models.SmallIntegerField(default=0, verbose_name='排序')),
                ('is_anonymous', models.BooleanField(default=0, verbose_name='是否匿名')),
                ('score', models.FloatField(default=10.0, verbose_name='商品评分')),
                ('score_deliver', models.FloatField(default=10.0, verbose_name='配送服务分')),
                ('score_package', models.FloatField(default=10.0, verbose_name='快递包装分')),
                ('score_speed', models.FloatField(default=10.0, verbose_name='送货速度分')),
                ('is_valid', models.BooleanField(default=True, verbose_name='是否有效')),
                ('product', models.ForeignKey(on_delete=True, related_name='comments', to='mall.Product', verbose_name='商品')),
                ('user', models.ForeignKey(on_delete=True, related_name='comments', to='accounts.User', verbose_name='用户')),
            ],
            options={
                'db_table': 'mall_comments',
            },
        ),
    ]
