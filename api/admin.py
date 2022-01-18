from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Leads, Subscription

# class AdminUser(admin.ModelAdmin):
#     def has_delete_permission(self, request, obj=None):
#         return True if request.is_superuser else False


admin.site.register(get_user_model())
admin.site.register(Leads)
admin.site.register(Subscription)


