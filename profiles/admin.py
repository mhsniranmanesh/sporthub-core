from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _
from profiles.models import User


# class CustomUserAdmin(UserAdmin):
#     list_display = ('username', 'first_name', 'last_name', 'email', 'phone_number','is_staff', 'balance')
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
#         (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
#                                        'groups', 'user_permissions')}),
#         (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
#         (_('Accounting Info'), {'fields': ('balance')}),
#     )
#
# admin.site.register(User, CustomUserAdmin)

admin.site.register(User, UserAdmin)