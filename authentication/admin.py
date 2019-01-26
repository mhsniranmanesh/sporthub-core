from django.contrib import admin

# Register your models here.
from authentication.models.passwordReset import PasswordReset

admin.site.register(PasswordReset)
