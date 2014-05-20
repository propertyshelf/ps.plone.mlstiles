# -*- coding: utf-8 -*-
"""Test Setup of ps.plone.mlstiles."""

# python imports
import unittest2 as unittest

# local imports
from ps.plone.mlstiles.testing import PS_PLONE_MLSTILES_INTEGRATION_TESTING


class TestSetup(unittest.TestCase):
    """Validata setup process for ps.plone.mlstiles."""

    layer = PS_PLONE_MLSTILES_INTEGRATION_TESTING

    def setUp(self):
        """Additional test setup."""
        self.app = self.layer['app']
        self.portal = self.layer['portal']

    def test_product_is_installed(self):
        """Validate that our product is installed."""
        qi = self.portal.portal_quickinstaller
        self.assertTrue(qi.isProductInstalled('ps.plone.mlstiles'))

    def test_collective_cover_installed(self):
        """Validate that collective.cover is installed."""
        qi = self.portal.portal_quickinstaller
        self.assertTrue(qi.isProductInstalled('collective.cover'))

    def test_plone_mls_listing_installed(self):
        """Validate that plone.mls.listing is installed."""
        qi = self.portal.portal_quickinstaller
        self.assertTrue(qi.isProductInstalled('plone.mls.listing'))
