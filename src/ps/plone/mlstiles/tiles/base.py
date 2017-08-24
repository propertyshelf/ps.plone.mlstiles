# -*- coding: utf-8 -*-
"""Base and helper classes for tiles."""

# zope imports
from plone.app.vocabularies.catalog import CatalogSource as CatalogSourceBase


class CatalogSource(CatalogSourceBase):
    """Specific catalog source to allow targeted widget."""

    def __contains__(self, value):
        """Return always contains to allow lazy handling of removed objs."""
        return True
