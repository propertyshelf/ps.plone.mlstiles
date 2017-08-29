# -*- coding: utf-8 -*-
"""A tile that shows a list of MLS developments."""

# zope import
from plone.supermodel.model import Schema
from plone.tiles import Tile
from ps.plone.mls import (
    # api,
    config,
)
from ps.plone.mls.interfaces import IDevelopmentCollection
from zope import schema
from zope.annotation.interfaces import IAnnotations

# local imports
from ps.plone.mlstiles import _


class IDevelopmentCollectionTile(Schema):
    """Configuration schema for a development collection tile."""

    count = schema.Int(
        default=5,
        required=False,
        title=_(u'Number of items to display'),
    )

    offset = schema.Int(
        default=0,
        required=False,
        title=_(u'Start at item'),
    )


class DevelopmentCollectionTile(Tile):
    """A tile that shows a list of MLS developments."""

    def get_config(self, obj):
        """Get collection configuration data from annotations."""
        annotations = IAnnotations(obj)
        return annotations.get(config.SETTINGS_DEVELOPMENT_COLLECTION, {})

    def has_development_collection(self, obj):
        """Check if the obj is activated for recent MLS developments."""
        return IDevelopmentCollection.providedBy(obj)
