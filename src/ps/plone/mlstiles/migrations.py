# -*- coding: utf-8 -*-
"""Migration steps for ps.plone.mlstiles."""

# zope imports
from plone import api

# local imports
from ps.plone.mls import config


def migrate_to_1001(context):
    """Migrate from 1000 to 1001.

    * Install ps.plone.mls
    * Add featured listings tile.
    """
    setup = api.portal.get_tool(name='portal_setup')
    qi = api.portal.get_tool(name='portal_quickinstaller')

    qi.installProduct('ps.plone.mls')
    setup.runImportStepFromProfile(config.PROFILE_ID, 'plone.app.registry')


def migrate_to_1002(context):
    """Migrate from 1001 to 1002.

    * Add development collection tile.
    """
    setup = api.portal.get_tool(name='portal_setup')
    setup.runImportStepFromProfile(config.PROFILE_ID, 'plone.app.registry')
