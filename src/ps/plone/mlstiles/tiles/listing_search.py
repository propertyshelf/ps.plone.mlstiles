# -*- coding: utf-8 -*-
"""A tile that shows a search form for listings."""

# zope imports
from Products.CMFPlone import PloneMessageFactory as PMF
from plone.directives import form
from plone.mls.listing.browser.listing_search import (
    CONFIGURATION_KEY,
    IListingSearch,
    IListingSearchForm,
)
from plone.mls.listing.browser.valuerange.widget import ValueRangeFieldWidget
from plone.supermodel.model import Schema
from plone.tiles import Tile
from z3c.form import button, field
from z3c.form.browser import checkbox, radio
from zope.annotation.interfaces import IAnnotations


class ListingSearchForm(form.Form):
    """Listing Search Form."""

    fields = field.Fields(IListingSearchForm)
    ignoreContext = True
    method = 'get'
    search_url = None

    fields['air_condition'].widgetFactory = radio.RadioFieldWidget
    fields['baths'].widgetFactory = ValueRangeFieldWidget
    fields['lot_size'].widgetFactory = ValueRangeFieldWidget
    fields['interior_area'].widgetFactory = ValueRangeFieldWidget
    fields['beds'].widgetFactory = ValueRangeFieldWidget
    fields['geographic_type'].widgetFactory = checkbox.CheckBoxFieldWidget
    fields['jacuzzi'].widgetFactory = radio.RadioFieldWidget
    fields['listing_type'].widgetFactory = checkbox.CheckBoxFieldWidget
    fields['location_type'].widgetFactory = checkbox.CheckBoxFieldWidget
    fields['object_type'].widgetFactory = checkbox.CheckBoxFieldWidget
    fields['ownership_type'].widgetFactory = checkbox.CheckBoxFieldWidget
    fields['pool'].widgetFactory = radio.RadioFieldWidget
    fields['view_type'].widgetFactory = checkbox.CheckBoxFieldWidget

    def __init__(self, context, request):
        super(ListingSearchForm, self).__init__(context, request)
        form_context = self.getContent()
        if form_context is not None:
            self.prefix = 'form.{0}'.format(form_context.id)

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


class IListingSearchTile(Schema):
    """Configuration schema for a listing search tile."""


class ListingSearchTile(Tile):
    """A tile that shows a search form for listings."""

    def get_config(self, obj):
        """Get collection configuration data from annotations."""
        annotations = IAnnotations(obj)
        return annotations.get(CONFIGURATION_KEY, {})

    def has_listing_search(self, obj):
        """Check if the obj is activated for a listing search."""
        return IListingSearch.providedBy(obj)
