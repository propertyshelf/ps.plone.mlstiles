# -*- coding: utf-8 -*-
"""A tile that shows a list of MLS developments for plone.app.mosaic."""

# zope imports
from zope import schema

# local imports
from ps.plone.mlstiles import _
from ps.plone.mlstiles.tiles.base import CatalogSource
from ps.plone.mlstiles.tiles.development_collection import (
    IDevelopmentCollectionTile as IDevelopmentCollectionTileBase,
    DevelopmentCollectionTile as DevelopmentCollectionTileBase,
)


class IDevelopmentCollectionTile(IDevelopmentCollectionTileBase):
    """Configuration schema for a development collection."""

    content_uid = schema.Choice(
        title=_(u'Select an existing content'),
        required=True,
        source=CatalogSource(),
    )


class DevelopmentCollectionTile(DevelopmentCollectionTileBase):
    """A tile that shows a list of MLS developments."""
