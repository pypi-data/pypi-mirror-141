# -*- coding: utf-8
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AuthBackendPamConfig(AppConfig):
    name = "auth_backend_pam"
    verbose_name = _("auth_backend_pam")
