from django.contrib import admin
from .models import Offer

class OfferAdmin(admin.ModelAdmin):
    list_display = ('get_seller_code', 'get_name', 'get_order_paid_status')

    def get_seller_code(self, obj):
        return obj.params.get('sellerCode', 'N/A')
    get_seller_code.short_description = 'Seller Code'

    def get_name(self, obj):
        return obj.params.get('name', 'N/A')
    get_name.short_description = 'Name'

    def get_order_paid_status(self, obj):
        return obj.order.paid if obj.order else 'No Order'
    get_order_paid_status.short_description = 'Order Paid'

admin.site.register(Offer, OfferAdmin)