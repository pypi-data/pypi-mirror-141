# -*- coding: utf-8 -*-
""" Setup script of LDAP authentication backend for Django """

from setuptools import setup

setup(
		name="django-ldap-auth-backend",
		version="0.3.3",  # REV-CONSTANT:rev 5d022db7d38f580a850cd995e26a6c2f
		description="LDAP authentication backend for Django",
		packages=[
				"ldapauthbackend",
				"ldapauthbackend.migrations",
		],
		include_package_data=True,
		install_requires=[
				"python-ldap >= 3.4.0, < 4.0.0",
				"django-angular-host-page-template-backend >= 0.3.0, < 0.4.0",
		],
		classifiers=[
				'Development Status :: 5 - Production/Stable',
				'Intended Audience :: Developers',
				'License :: OSI Approved :: MIT License',
				'Programming Language :: Python :: 3.7',
				'Framework :: Django :: 3.2',
		],
		license='MIT License',
)

# vim: ts=4 sw=4 ai nowrap
