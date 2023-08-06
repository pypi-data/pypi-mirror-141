from django.utils.translation import gettext_lazy as _
from django.conf import settings

def get_default_global_sidebar(request):
    return [
        {
            "title": _("Home"),
            "icon": "fa fa-home",
            "url": getattr(settings, "ADMIN_SITE_HOME_URL", "/admin/"),
        },
        {
            "title": _("Django Site Warnings"),
            "icon": "fa fa-box-open",
            "children": [
                {
                    "title": _("Warnings"),
                    "icon": "fa fa-boxes",
                    "model": "django_site_warnings.warning",
                    "permissions": ["django_site_warnings.view_warning"],
                },
                {
                    "title": _("Warning Categories"),
                    "icon": "fa fa-boxes",
                    "model": "django_site_warnings.waringcategory",
                    "permissions": ["django_site_warnings.view_waringcategory"],
                },
            ],
        },
        {
            "title": _("System Settings"),
            "icon": "fas fa-cogs",
            "children": [
                {
                    "title": _("User Manage"),
                    "icon": "fas fa-user",
                    "model": "auth.user",
                    "permissions": ["auth.view_user"],
                },
                {
                    "title": _("Group Manage"),
                    "icon": "fas fa-users",
                    "model": "auth.group",
                    "permissions": ["auth.view_group"],
                },
            ]
        }
    ]
