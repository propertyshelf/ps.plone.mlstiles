# -*- coding: utf-8 -*-
"""A tile that shows a list of MLS listings."""

# zope imports
from plone.mls.listing.browser.listing_collection import (
    CONFIGURATION_KEY as LC_CONFIGURATION_KEY,
    IListingCollection,
)
from plone.mls.listing.browser.recent_listings import (
    CONFIGURATION_KEY as RL_CONFIGURATION_KEY,
    IRecentListings,
)
from plone.supermodel.model import Schema
from plone.tiles import Tile
from ps.plone.mls.browser.listings import featured
from zope import schema
from zope.annotation.interfaces import IAnnotations
from zope.schema.fieldproperty import FieldProperty

# local imports
from ps.plone.mlstiles import _
from ps.plone.mlstiles.tiles.base import CatalogSource


class IListingCollectionTile(Schema):
    """Configuration schema for a listing collection tile."""

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


class ListingCollectionTile(Tile):
    """A tile that shows a list of MLS listings."""

    count = FieldProperty(IListingCollectionTile['count'])
    offset = FieldProperty(IListingCollectionTile['offset'])
    content_uid = FieldProperty(IListingCollectionTile['content_uid'])

    def get_config(self, obj):
        """Get collection configuration data from annotations."""
        annotations = IAnnotations(obj)
        return annotations.get(LC_CONFIGURATION_KEY, {})

    def has_listing_collection(self, obj):
        """Check if the obj is activated for recent MLS listings."""
        return IListingCollection.providedBy(obj)


class RecentListingsTile(ListingCollectionTile):
    """A tile that shows a list of recent MLS listings."""

    def get_config(self, obj):
        """Get collection configuration data from annotations."""
        annotations = IAnnotations(obj)
        return annotations.get(RL_CONFIGURATION_KEY, {})

    def has_listing_collection(self, obj):
        """Check if the obj is activated for recent MLS listings."""
        return IRecentListings.providedBy(obj)


class FeaturedListingsTile(ListingCollectionTile):
    """A tile that shows a list of featured MLS listings."""

    def get_config(self, obj):
        """Get collection configuration data from annotations."""
        annotations = IAnnotations(obj)
        return annotations.get(featured.CONFIGURATION_KEY, {})

    def has_listing_collection(self, obj):
        """Check if the obj is activated for recent MLS listings."""
        return featured.IFeaturedListings.providedBy(obj)
