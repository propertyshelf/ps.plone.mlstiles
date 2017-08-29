# -*- coding: utf-8 -*-
"""A tile that shows a list of MLS developments for plone.app.mosaic."""

# zope imports
from ps.plone.mls.interfaces import IDevelopmentCollection
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
        required=True,
        source=CatalogSource(
            object_provides=IDevelopmentCollection.__identifier__,
            path={
                'query': [''],
                'depth': -1,
            },
        ),
        title=_(u'Select an existing development collection'),
    )

    show_title = schema.Bool(
        default=True,
        required=False,
        title=_(u'Show development title'),
    )

    show_description = schema.Bool(
        default=True,
        required=False,
        title=_(u'Show development description'),
    )

    show_banner = schema.Bool(
        default=True,
        required=False,
        title=_(u'Show development banner image'),
    )

    show_logo = schema.Bool(
        default=True,
        required=False,
        title=_(u'Show development logo'),
    )

    show_location = schema.Bool(
        default=True,
        required=False,
        title=_(u'Show location information for a development'),
    )

    show_lot_size = schema.Bool(
        default=True,
        required=False,
        title=_(u'Show lot size information for a development'),
    )

    show_location_type = schema.Bool(
        default=True,
        required=False,
        title=_(u'Show location type information for a development'),
    )

    show_number_of_listings = schema.Bool(
        default=True,
        required=False,
        title=_(u'Show number of listings for a development'),
    )

    show_number_of_groups = schema.Bool(
        default=True,
        required=False,
        title=_(u'Show number of groups for a development'),
    )


class DevelopmentCollectionTile(DevelopmentCollectionTileBase):
    """A tile that shows a list of MLS developments."""
