# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models


class LDAPUserProfile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	dn = models.CharField(max_length=255)
	account_uid = models.BigIntegerField(default=-1)
	account_name = models.CharField(max_length=127)
	import_staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="+", editable=False)

	def __unicode__(self):
		return (f"LDAPUserProfile(user={self.user!r}, dn={self.dn}, "
				f"account_uid={self.account_uid}, account_name={self.account_name!r}, import_staff={self.import_staff!r})")
