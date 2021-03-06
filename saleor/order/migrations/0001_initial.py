# Generated by Django 2.0.8 on 2018-09-20 17:14

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_measurement.models
import django_prices.models
import jsonfield.fields
import saleor.core.weight


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0001_initial'),
        ('discount', '0001_initial'),
        ('shipping', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fulfillment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fulfillment_order', models.PositiveIntegerField(editable=False)),
                ('status', models.CharField(choices=[('fulfilled', 'Fulfilled'), ('canceled', 'Canceled')], default='fulfilled', max_length=32)),
                ('tracking_number', models.CharField(blank=True, default='', max_length=255)),
                ('shipping_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='FulfillmentLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(999)])),
                ('fulfillment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lines', to='order.Fulfillment')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('unfulfilled', 'Unfulfilled'), ('partially fulfilled', 'Partially fulfilled'), ('fulfilled', 'Fulfilled'), ('canceled', 'Canceled')], default='unfulfilled', max_length=32)),
                ('language_code', models.CharField(default='en', max_length=35)),
                ('tracking_client_id', models.CharField(blank=True, editable=False, max_length=36)),
                ('user_email', models.EmailField(blank=True, default='', max_length=254)),
                ('shipping_price_net', django_prices.models.MoneyField(currency='USD', decimal_places=2, default=0, editable=False, max_digits=12)),
                ('shipping_price_gross', django_prices.models.MoneyField(currency='USD', decimal_places=2, default=0, editable=False, max_digits=12)),
                ('shipping_method_name', models.CharField(blank=True, default=None, editable=False, max_length=255, null=True)),
                ('token', models.CharField(blank=True, max_length=36, unique=True)),
                ('total_net', django_prices.models.MoneyField(currency='USD', decimal_places=2, default=0, max_digits=12)),
                ('total_gross', django_prices.models.MoneyField(currency='USD', decimal_places=2, default=0, max_digits=12)),
                ('discount_amount', django_prices.models.MoneyField(currency='USD', decimal_places=2, default=0, max_digits=12)),
                ('discount_name', models.CharField(blank=True, default='', max_length=255)),
                ('translated_discount_name', models.CharField(blank=True, default='', max_length=255)),
                ('display_gross_prices', models.BooleanField(default=True)),
                ('customer_note', models.TextField(blank=True, default='')),
                ('weight', django_measurement.models.MeasurementField(default=saleor.core.weight.zero_weight, measurement_class='Mass')),
                ('imp_uid', models.CharField(blank=True, max_length=100)),
                ('imp_status', models.CharField(choices=[('ready', '미결제'), ('paid', '결제완료'), ('cancelled', '결제취소'), ('failed', '결제실패')], db_index=True, default='ready', max_length=9)),
                ('billing_address', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='account.Address')),
                ('shipping_address', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='account.Address')),
                ('shipping_method', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='shipping.ShippingMethod')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to=settings.AUTH_USER_MODEL)),
                ('voucher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='discount.Voucher')),
            ],
            options={
                'ordering': ('-pk',),
                'permissions': (('manage_orders', 'Manage orders.'),),
            },
        ),
        migrations.CreateModel(
            name='OrderEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('type', models.CharField(choices=[('PLACED', 'placed'), ('PLACED_FROM_DRAFT', 'draft_placed'), ('ORDER_MARKED_AS_PAID', 'marked_as_paid'), ('CANCELED', 'canceled'), ('ORDER_FULLY_PAID', 'order_paid'), ('UPDATED', 'updated'), ('EMAIL_SENT', 'email_sent'), ('PAYMENT_CAPTURED', 'captured'), ('PAYMENT_REFUNDED', 'refunded'), ('PAYMENT_RELEASED', 'released'), ('FULFILLMENT_CANCELED', 'fulfillment_canceled'), ('FULFILLMENT_RESTOCKED_ITEMS', 'restocked_items'), ('FULFILLMENT_FULFILLED_ITEMS', 'fulfilled_items'), ('NOTE_ADDED', 'note_added'), ('OTHER', 'other')], max_length=255)),
                ('parameters', jsonfield.fields.JSONField(blank=True, default={})),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='order.Order')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('date',),
            },
        ),
        migrations.CreateModel(
            name='OrderLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=386)),
                ('translated_product_name', models.CharField(default='', max_length=386)),
                ('product_sku', models.CharField(max_length=32)),
                ('is_shipping_required', models.BooleanField()),
                ('quantity', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(999)])),
                ('quantity_fulfilled', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(999)])),
                ('unit_price_net', django_prices.models.MoneyField(currency='USD', decimal_places=2, max_digits=12)),
                ('unit_price_gross', django_prices.models.MoneyField(currency='USD', decimal_places=2, max_digits=12)),
                ('tax_rate', models.DecimalField(decimal_places=2, default='0.0', max_digits=5)),
                ('order', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='lines', to='order.Order')),
                ('variant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='product.ProductVariant')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variant', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('waiting', 'Waiting for confirmation'), ('preauth', 'Pre-authorized'), ('confirmed', 'Confirmed'), ('rejected', 'Rejected'), ('refunded', 'Refunded'), ('error', 'Error'), ('input', 'Input')], default='waiting', max_length=10)),
                ('fraud_status', models.CharField(choices=[('unknown', 'Unknown'), ('accept', 'Passed'), ('reject', 'Rejected'), ('review', 'Review')], default='unknown', max_length=10, verbose_name='fraud check')),
                ('fraud_message', models.TextField(blank=True, default='')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('transaction_id', models.CharField(blank=True, max_length=255)),
                ('currency', models.CharField(max_length=10)),
                ('total', models.DecimalField(decimal_places=2, default='0.0', max_digits=9)),
                ('delivery', models.DecimalField(decimal_places=2, default='0.0', max_digits=9)),
                ('tax', models.DecimalField(decimal_places=2, default='0.0', max_digits=9)),
                ('description', models.TextField(blank=True, default='')),
                ('billing_first_name', models.CharField(blank=True, max_length=256)),
                ('billing_last_name', models.CharField(blank=True, max_length=256)),
                ('billing_address_1', models.CharField(blank=True, max_length=256)),
                ('billing_address_2', models.CharField(blank=True, max_length=256)),
                ('billing_city', models.CharField(blank=True, max_length=256)),
                ('billing_postcode', models.CharField(blank=True, max_length=256)),
                ('billing_country_code', models.CharField(blank=True, max_length=2)),
                ('billing_country_area', models.CharField(blank=True, max_length=256)),
                ('billing_email', models.EmailField(blank=True, max_length=254)),
                ('customer_ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('extra_data', models.TextField(blank=True, default='')),
                ('message', models.TextField(blank=True, default='')),
                ('token', models.CharField(blank=True, default='', max_length=36)),
                ('captured_amount', models.DecimalField(decimal_places=2, default='0.0', max_digits=9)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payments', to='order.Order')),
            ],
            options={
                'ordering': ('-pk',),
            },
        ),
        migrations.AddField(
            model_name='fulfillmentline',
            name='order_line',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='order.OrderLine'),
        ),
        migrations.AddField(
            model_name='fulfillment',
            name='order',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='fulfillments', to='order.Order'),
        ),
    ]
