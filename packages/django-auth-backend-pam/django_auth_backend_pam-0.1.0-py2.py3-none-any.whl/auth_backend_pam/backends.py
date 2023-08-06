import logging

import pam
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import RemoteUserBackend

logger = logging.getLogger(__name__)
UserModel = get_user_model()


class PamBackend(RemoteUserBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        logger.debug(
            "%s: authenticate username = %s" % (self.__class__.__name__, username)
        )
        user = None
        if pam.authenticate(username, password):
            user = super().authenticate(request, username)
            if user is not None:
                user.is_active = settings.PAM_USERS["is_active"]
                user.is_staff = settings.PAM_USERS["is_staff"]
                user.is_superuser = settings.PAM_USERS["is_superuser"]
                user.save()
        return user if self.user_can_authenticate(user) else None
