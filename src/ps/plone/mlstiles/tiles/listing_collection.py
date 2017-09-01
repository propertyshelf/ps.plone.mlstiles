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
from ps.plone.mls.browser.listings import featured
from zope.annotation.interfaces import IAnnotations


class ListingCollectionTileMixin(object):
    """A tile that shows a list of MLS listings."""

    def get_config(self, obj):
        """Get collection configuration data from annotations."""
        annotations = IAnnotations(obj)
        return annotations.get(LC_CONFIGURATION_KEY, {})

    def has_listing_collection(self, obj):
        """Check if the obj is activated for recent MLS listings."""
        return IListingCollection.providedBy(obj)


class RecentListingsTileMixin(ListingCollectionTileMixin):
    """A tile that shows a list of recent MLS listings."""

    def get_config(self, obj):
        """Get collection configuration data from annotations."""
        annotations = IAnnotations(obj)
        return annotations.get(RL_CONFIGURATION_KEY, {})

    def has_listing_collection(self, obj):
        """Check if the obj is activated for recent MLS listings."""
        return IRecentListings.providedBy(obj)


class FeaturedListingsTileMixin(ListingCollectionTileMixin):
    """A tile that shows a list of featured MLS listings."""

    def get_config(self, obj):
        """Get collection configuration data from annotations."""
        annotations = IAnnotations(obj)
        return annotations.get(featured.CONFIGURATION_KEY, {})

    def has_listing_collection(self, obj):
        """Check if the obj is activated for recent MLS listings."""
        return featured.IFeaturedListings.providedBy(obj)
