from django.contrib import admin
from .models import Offer

class OfferAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'get_seller_code', 'get_order_paid_status', 'get_order_payment_id')

    def get_seller_code(self, obj):
        return obj.params.get('sellerCode', 'N/A')
    get_seller_code.short_description = 'Seller Code'

    def get_name(self, obj):
        return obj.params.get('name', 'N/A')
    get_name.short_description = 'Name'

    def get_order_paid_status(self, obj):
        return obj.order.paid if obj.order else 'No Order'
    get_order_paid_status.short_description = 'Order Paid'

    def get_order_payment_id(self, obj):
        return obj.order.payment_id if obj.order else 'No Order'
    get_order_payment_id.short_description = 'Payment id'

admin.site.register(Offer, OfferAdmin)