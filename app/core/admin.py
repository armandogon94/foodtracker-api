from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext as _

from . import models


class UserAdmin(BaseUserAdmin):
    # Used for listing all users screen
    ordering = ['id']
    list_display = ['email', 'public_name', 'first_name', 'last_name',
                    'is_foodtruck', 'date_joined', 'last_login']

    # Used for editing a user screen
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('public_name',)}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'is_foodtruck',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )

    # Used for adding a new user screen
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('public_name', 'email', 'password1', 'password2',)
        }),
    )

    search_fields = ('email', 'public_name', 'first_name', 'last_name',)


admin.site.register(models.User, UserAdmin)
