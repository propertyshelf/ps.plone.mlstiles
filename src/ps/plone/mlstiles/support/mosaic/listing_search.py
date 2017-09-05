# -*- coding: utf-8 -*-
"""Tiles that shows a list of MLS listings for plone.app.mosaic."""

# zope imports
from plone import api
from plone.app.standardtiles import _PMF
from plone.mls.listing.browser.listing_search import IListingSearch
from plone.memoize import view
from plone.supermodel.model import Schema
from plone.tiles import Tile
from zope import schema

# local imports
from ps.plone.mlstiles import _
from ps.plone.mlstiles.tiles.base import CatalogSource
from ps.plone.mlstiles.tiles.listing_search import ListingSearchTileMixin


class IListingSearchTile(Schema):
    """Configuration schema for a listing search tile."""

    content_uid = schema.Choice(
        required=True,
        source=CatalogSource(
            object_provides=IListingSearch.__identifier__,
            path={
                'query': [''],
                'depth': -1,
            },
        ),
        title=_(u'Select an existing listing search'),
    )

    tile_title = schema.TextLine(
        required=False,
        title=_PMF(u'Title'),
    )

    show_tile_title = schema.Bool(
        default=True,
        required=False,
        title=_PMF(u'Show tile title'),
    )

    tile_title_level = schema.Choice(
        default=u'h2',
        required=False,
        title=_(u'Headline level'),
        values=(u'h1', u'h2', u'h3', u'h4', u'h5', u'h6'),
    )

    show_more_link = schema.Bool(
        default=True,
        required=False,
        title=_(u'Show link to search page'),
    )

    more_link_text = schema.TextLine(
        default=_(u'Advanced Search'),
        required=False,
        title=_(u'Text for link to search page'),
    )

    tile_class = schema.TextLine(
        default=u'',
        description=_PMF(
            u'Insert a list of additional CSS classes that will ',
            u'be added to the tile',
        ),
        required=False,
        title=_PMF(u'Tile additional styles'),
    )


class ListingSearchTile(ListingSearchTileMixin, Tile):
    """A tile that shows a list of MLS listings."""

    @property
    def tile_class(self):
        css_class = 'listing__form'
        additional_classes = self.data.get('tile_class', '')
        if not additional_classes:
            return css_class
        return ' '.join([css_class, additional_classes])

    @property
    @view.memoize
    def get_context(self):
        """Return the listing collection context."""
        uuid = self.data.get('content_uid')
        if uuid != api.content.get_uuid(obj=self.context):
            item = api.content.get(UID=uuid)
            if item is not None:
                return item
        return None

    @property
    def available_fields(self):
        fields = []
        return fields
