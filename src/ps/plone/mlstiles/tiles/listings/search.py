# -*- coding: utf-8 -*-
"""MLS listing search tile."""

# zope imports
from Acquisition import aq_inner
from Products.CMFPlone import PloneMessageFactory as PMF
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.cover import _ as _cc
from collective.cover.tiles import base
from plone.app.uuid.utils import uuidToObject
from plone.directives import form
from plone.mls.listing.browser import listing_search
from plone.tiles.interfaces import ITileDataManager
from plone.uuid.interfaces import IUUID
from z3c.form import field, button
from zope import schema
from zope.annotation.interfaces import IAnnotations
from zope.interface import alsoProvides, implementer
from zope.schema.fieldproperty import FieldProperty

# starting from 0.6.0 version plone.z3cform has IWrappedForm interface
try:
    from plone.z3cform.interfaces import IWrappedForm
    HAS_WRAPPED_FORM = True
except ImportError:
    HAS_WRAPPED_FORM = False

# local imports
from ps.plone.mlstiles import _


class ListingSearchForm(form.Form):
    """Listing Search Form."""
    fields = field.Fields(listing_search.IListingSearchForm)
    ignoreContext = True
    method = 'get'
    search_url = None

    @property
    def action(self):
        """See interfaces.IInputForm"""
        if self.search_url:
            return self.search_url
        return super(ListingSearchForm, self).action()

    @button.buttonAndHandler(
        PMF(u'label_search', default=u'Search'),
        name='search',
    )
    def handle_search(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return


class IListingSearchTile(base.IPersistentCoverTile):
    """Configuration schema for a listing search."""

    header = schema.TextLine(
        required=False,
        title=_cc(u'Header'),
    )

    footer = schema.TextLine(
        required=False,
        title=_cc(u'Footer'),
    )

    uuid = schema.TextLine(
        readonly=True,
        title=_cc(u'UUID'),
    )


@implementer(IListingSearchTile)
class ListingSearchTile(base.PersistentCoverTile):
    """A tile that shows a search form for listings."""

    is_configurable = True
    is_editable = True
    short_name = _(u'MLS: Listing Search')
    index = ViewPageTemplateFile('search.pt')

    header = FieldProperty(IListingSearchTile['header'])
    footer = FieldProperty(IListingSearchTile['footer'])
    uuid = FieldProperty(IListingSearchTile['uuid'])

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

    def remove_relation(self):
        data_mgr = ITileDataManager(self)
        old_data = data_mgr.get()
        if 'uuid' in old_data:
            old_data.pop('uuid')
        data_mgr.set(old_data)

    def show_header(self):
        return self._field_is_visible('header')

    @property
    def form(self):
        uuid = self.data.get('uuid', None)
        obj = uuidToObject(uuid)
        if not self.has_listing_search(obj):
            return
        form = ListingSearchForm(aq_inner(obj), self.request)
        form.search_url = self.search_url()
        if HAS_WRAPPED_FORM:
            alsoProvides(form, IWrappedForm)
        form.update()
        return form

    def search_url(self):
        uuid = self.data.get('uuid', None)
        obj = uuidToObject(uuid)
        return obj.absolute_url() if obj else ''

    def show_footer(self):
        return self._field_is_visible('footer')
