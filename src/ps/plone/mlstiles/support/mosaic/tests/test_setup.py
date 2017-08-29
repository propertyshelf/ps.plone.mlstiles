# -*- coding: utf-8 -*-
"""Test Setup of ps.plone.mlstiles."""

# python imports
import unittest

# zope imports
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

# local imports
from ps.plone.mlstiles.testing import (
    PS_PLONE_MLSTILES_INTEGRATION_TESTING,
    skip_if_no_mosaic,
)


class TestSetup(unittest.TestCase):
    """Validate setup process for ps.plone.mlstiles."""

    layer = PS_PLONE_MLSTILES_INTEGRATION_TESTING

    def setUp(self):
        """Additional test setup."""
        self.app = self.layer['app']
        self.portal = self.layer['portal']

    @skip_if_no_mosaic
    def test_plone_app_mosaic_installed(self):
        """Validate that plone.app.mosaic is installed."""
        qi = self.portal.portal_quickinstaller
        self.assertTrue(qi.isProductInstalled('plone.app.mosaic'))

    @skip_if_no_mosaic
    def test_tiles_registered(self):
        """Validate that the tiles are registered."""
        registry = getUtility(IRegistry)
        key = 'plone.app.tiles'
        self.assertIn(
            'ps.plone.mlstiles.mosaic.development_collection',
            registry.records.get(key).value,
        )

    @skip_if_no_mosaic
    def test_tiles_available(self):
        """Validate that the tiles are available for plone.app.mosaic."""
        registry = getUtility(IRegistry)
        base_key = 'plone.app.mosaic.app_tiles'
        key = base_key + '.ps_plone_mlstiles_development_collection.name'
        self.assertIn(
            'ps.plone.mlstiles.mosaic.development_collection',
            registry.records.get(key).value,
        )
