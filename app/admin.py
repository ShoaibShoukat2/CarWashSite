from django.contrib import admin
from .models import *



@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title','description','admin_name', 'category_name')

    def admin_name(self, obj):
        return obj.admin.user.username if obj.admin.user else None
    
    admin_name.short_description = 'Admin'



    def category_name(self, obj):
        return obj.category.name if obj.category else None
    
    category_name.short_description = 'Category'



admin.site.register(Comments)



class AdminAdmin(admin.ModelAdmin):
    list_display = ('user',)

admin.site.register(Admin, AdminAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'admin')

admin.site.register(Category, CategoryAdmin)




@admin.register(Signup)
class SignupAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'phone_number', 'vehicle_brand', 'vehicle_model', 'vehicle_type', 'created_at')
    list_display_links = ('id', 'email')  # Make 'id' and 'email' clickable
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')  # Add search functionality



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



class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'user_email', 'subscription', 'package', 'vehicle', 'price')
    # Add more fields as needed

admin.site.register(UserProfile, UserProfileAdmin)


class AppointmentScheduleAdmin(admin.ModelAdmin):
    list_display = ('location', 'date', 'user_id')
    search_fields = ('location', 'user_id__username')  # Assuming 'Signup' has a 'username' field

# Register your models with the admin site
admin.site.register(AppoitmentSchedule, AppointmentScheduleAdmin)


