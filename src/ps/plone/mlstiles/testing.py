# -*- coding: utf-8 -*-
"""Test Layer for ps.plone.mlstiles."""

# zope imports
from plone.app.testing import (
    IntegrationTesting,
    PloneSandboxLayer,
    PLONE_FIXTURE,
    applyProfile,
)
from zope.configuration import xmlconfig


class PSPloneMLSTiles(PloneSandboxLayer):
    """Custom Test Layer for ps.plone.mlstiles."""
    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        """Set up Zope for testing."""
        # Load ZCML
        import ps.plone.mlstiles
        xmlconfig.file(
            'configure.zcml',
            ps.plone.mlstiles,
            context=configurationContext,
        )

    def setUpPloneSite(self, portal):
        """Set up a Plone site for testing."""
        applyProfile(portal, 'ps.plone.mlstiles:default')


PS_PLONE_MLSTILES_FIXTURE = PSPloneMLSTiles()
PS_PLONE_MLSTILES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PS_PLONE_MLSTILES_FIXTURE, ),
    name='PSPloneMLSTiles:Integration',
)
