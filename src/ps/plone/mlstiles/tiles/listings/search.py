# -*- coding: utf-8 -*-
"""MLS listing search tile."""

# zope imports
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.cover import _ as _cc
from collective.cover.tiles import base
from plone.app.uuid.utils import uuidToObject
from plone.mls.listing.browser import listing_search
from plone.tiles.interfaces import (
    ITileDataManager,
    ITileType,
)
from plone.uuid.interfaces import IUUID
from zope import schema
from zope.annotation.interfaces import IAnnotations
from zope.component import queryUtility
from zope.interface import implementer
from zope.schema.fieldproperty import FieldProperty

# local imports
from ps.plone.mlstiles import _


class IListingSearchTile(base.IPersistentCoverTile):
    """Configuration schema for a listing search."""

    header = schema.TextLine(
        required=False,
        title=_cc(u'Header'),
    )


@implementer(IListingSearchTile)
class ListingSearchTile(base.PersistentCoverTile):
    """A tile that shows a search form for listings."""

    is_configurable = True
    is_editable = True
    short_name = _(u'MLS: Listing Search')
    index = ViewPageTemplateFile('search.pt')
    configured_fields = []

    header = FieldProperty(IListingSearchTile['header'])

    def get_title(self):
        return self.data['title']

    def has_listing_search(self, obj):
        """Check if the obj is activated for a listing search."""
        return listing_search.IListingSearch.providedBy(obj)

    def get_config(self, obj):
        """Get collection configuration data from annotations."""
        annotations = IAnnotations(obj)
        return annotations.get(listing_search.CONFIGURATION_KEY, {})

    def is_empty(self):
        return self.data.get('uuid', None) is None or \
            uuidToObject(self.data.get('uuid')) is None

    def populate_with_object(self, obj):
        # Check permission.
        super(ListingSearchTile, self).populate_with_object(obj)

        if obj.portal_type in self.accepted_ct():
            # Use obj's title as header.
            header = safe_unicode(obj.Title())
            footer = _cc(u'More…')
            uuid = IUUID(obj)

            data_mgr = ITileDataManager(self)
            data_mgr.set({
                'header': header,
                'footer': footer,
                'uuid': uuid,
            })

    def get_configured_fields(self):
        # Override this method, since we are not storing anything
        # in the fields, we just use them for configuration
        tileType = queryUtility(ITileType, name=self.__name__)
        conf = self.get_tile_configuration()

        fields = schema.getFieldsInOrder(tileType.schema)

        results = []
        for name, obj in fields:
            field = {'id': name,
                     'title': obj.title}
            if name in conf:
                field_conf = conf[name]
                if ('visibility' in field_conf and
                        field_conf['visibility'] == u'off'):
                    # If the field was configured to be invisible, then just
                    # ignore it
                    continue

                if 'htmltag' in field_conf:
                    # If this field has the capability to change its html tag
                    # render, save it here
                    field['htmltag'] = field_conf['htmltag']

            results.append(field)

        return results

    def remove_relation(self):
        data_mgr = ITileDataManager(self)
        old_data = data_mgr.get()
        if 'uuid' in old_data:
            old_data.pop('uuid')
        data_mgr.set(old_data)

    def show_header(self):
        return self._field_is_visible('header')

    def search_url(self):
        uuid = self.data.get('uuid', None)
        obj = uuidToObject(uuid)
        return obj.absolute_url() if obj else ''

    def show_footer(self):
        return self._field_is_visible('footer')
