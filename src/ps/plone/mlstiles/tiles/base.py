# -*- coding: utf-8 -*-
"""Base and helper classes for tiles."""

# zope imports
try:
    from plone.app.vocabularies.catalog import (
        CatalogSource as CatalogSourceBase,
    )
except ImportError:
    from plone.app.vocabularies.catalog import (
        SearchableTextSourceBinder as CatalogSourceBase,
    )


class CatalogSource(CatalogSourceBase):
    """Specific catalog source to allow targeted widget."""

    def __contains__(self, value):
        """Return always contains to allow lazy handling of removed objs."""
        return True
