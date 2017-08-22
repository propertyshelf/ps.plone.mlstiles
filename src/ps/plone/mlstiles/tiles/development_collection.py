# -*- coding: utf-8 -*-
"""A tile that shows a list of MLS developments."""

# zope import
from plone.app.vocabularies.catalog import CatalogSource as CatalogSourceBase
from plone.supermodel.model import Schema
from plone.tiles import Tile
from ps.plone.mls import (
    # api,
    config,
)
from ps.plone.mls.interfaces import IDevelopmentCollection
from zope import schema
from zope.annotation.interfaces import IAnnotations
from zope.schema.fieldproperty import FieldProperty

# local imports
from ps.plone.mlstiles import _


class CatalogSource(CatalogSourceBase):
    """Specific catalog source to allow targeted widget."""

    def __contains__(self, value):
        """Return always contains to allow lazy handling of removed objs."""
        return True


class IDevelopmentCollectionTile(Schema):
    """Configuration schema for a development collection tile."""

    count = schema.List(
        required=False,
        title=_(u'Number of items to display'),
        value_type=schema.TextLine(),
    )

    offset = schema.Int(
        default=0,
        required=False,
        title=_(u'Start at item'),
    )

    content_uid = schema.Choice(
        title=_(u'Select an existing content'),
        required=True,
        source=CatalogSource(),
    )


class DevelopmentCollectionTile(Tile):
    """A tile that shows a list of MLS developments."""

    count = FieldProperty(IDevelopmentCollectionTile['count'])
    offset = FieldProperty(IDevelopmentCollectionTile['offset'])
    content_uid = FieldProperty(IDevelopmentCollectionTile['content_uid'])

    def get_config(self, obj):
        """Get collection configuration data from annotations."""
        annotations = IAnnotations(obj)
        return annotations.get(config.SETTINGS_DEVELOPMENT_COLLECTION, {})

    def has_development_collection(self, obj):
        """Check if the obj is activated for recent MLS developments."""
        return IDevelopmentCollection.providedBy(obj)
