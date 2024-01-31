from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import (Note,NoteShared)

User = get_user_model()

@admin.register(User)
class UserAdmin(UserAdmin):
    empty_value_display = "--empty--"
    list_display = ("username","email")
    search_fields = ("username","email")
    date_hierarchy = "date_joined"
    search_help_text = "search by ..." 

    fieldsets = (
            (None, {"fields": ("username", "password")}),
            (_("Personal Info"), {"fields": ("first_name", "last_name", "email",)}),
            (
                _("Permissions"),
                {
                    "fields": (
                        "is_active",
                        "is_staff",
                        "is_superuser",
                        "groups",
                        "user_permissions",
                        ),
                    },
                ),
            (_("Important dates"), {"fields": ("last_login", "date_joined")}),
            )
    add_fieldsets = (
            (None, {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2")
                }),
            )

admin.site.register(Note)
admin.site.register(NoteShared)
