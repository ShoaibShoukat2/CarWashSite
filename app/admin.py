from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Signup)
class SignupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'created_at')
    search_fields = ('name', 'email',)
    list_filter = ('created_at',)




@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'file')


@admin.register(SubscrationDuration)
class SubscrationDurationAdmin(admin.ModelAdmin):
    list_display = ('get_vehicle_name','subscription_name',)



    def get_vehicle_name(self, obj):

        return obj.vehicle_id.name


    get_vehicle_name.short_description = 'Vehicle Name'


@admin.register(Packages)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('vehicle_name', 'subscription_name', 'name')


    def vehicle_name(self, obj):
        return obj.vehicle_id.name

    vehicle_name.short_description = 'Vehicle Name'

    def subscription_name(self, obj):
        return obj.subscription_id.subscription_name

    subscription_name.short_description = 'Subscription Name'



@admin.register(DescriptionPrice)
class DescriptionPriceAdmin(admin.ModelAdmin):
    list_display = ('get_vehicle_name', 'get_subscription_name', 'get_package_name', 'description', 'price')
    list_filter = ('vehicle_id', 'subscription_id', 'package_id')

    def get_vehicle_name(self, obj):
        return obj.vehicle_id.name
    get_vehicle_name.short_description = 'Vehicle Name'

    def get_subscription_name(self, obj):
        return obj.subscription_id.subscription_name
    get_subscription_name.short_description = 'Subscription Name'

    def get_package_name(self, obj):
        return obj.package_id.name
    get_package_name.short_description = 'Package Name'

