# -*- coding: utf-8 -*-
"""A tile that shows a list of MLS developments."""

# python imports
import copy

# zope import
from plone import api as plone_api
from plone.supermodel.model import Schema
from plone.memoize import view
from ps.plone.mls import (
    api,
    config,
)
from ps.plone.mls.browser.developments.collection import (
    EXCLUDED_SEARCH_FIELDS,
    FIELDS,
)
from ps.plone.mls.interfaces import IDevelopmentCollection
from zope import schema
from zope.annotation.interfaces import IAnnotations
from zope.traversing.browser.absoluteurl import absoluteURL

# local imports
from ps.plone.mlstiles import _


class IDevelopmentCollectionTileBase(Schema):
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


class DevelopmentCollectionTileMixin(object):
    """A tile mixin that shows a list of MLS developments."""

    def get_config(self, obj):
        """Get collection configuration data from annotations."""
        annotations = IAnnotations(obj)
        return annotations.get(config.SETTINGS_DEVELOPMENT_COLLECTION, {})

    def has_development_collection(self, obj):
        """Check if the obj is activated for recent MLS developments."""
        return IDevelopmentCollection.providedBy(obj)

    @property
    def get_context(self):
        """Return the development collection context."""
        raise NotImplementedError

    def get_fields(self):
        return FIELDS

    @property
    def count(self):
        raise NotImplementedError

    @property
    def offset(self):
        raise NotImplementedError

    @property
    @view.memoize
    def items(self):
        """Return the collection items."""
        items = []
        context = self.get_context
        if not context or not self.has_development_collection(context):
            return items

        context_config = copy.copy(self.get_config(context))
        language = plone_api.portal.get_current_language(context=context)
        mlsapi = api.get_api(context=context, lang=language)
        params = {
            'fields': u','.join(self.get_fields()),
            'limit': self.count,
            'offset': self.offset,
        }
        context_config.update(params)
        params = api.prepare_search_params(
            context_config,
            context=context,
            omit=EXCLUDED_SEARCH_FIELDS,
        )
        try:
            result = api.Development.search(mlsapi, params=params)
        except Exception:
            return items
        else:
            items = result.get_items()
        return items

    def get_item_url(self, item):
        """Get the (possibly modified) URL for the development item."""
        config = {}
        context = self.get_context
        if context and self.has_development_collection(context):
            config = copy.copy(self.get_config(context))

        url = u'{0}{1}'.format(self.view_url(context), item.id.value)
        if config.get('modify_url', True):
            url = u'{0}___{1}-{2}'.format(
                url,
                item.title.value,
                item.location.value,
            )
        return url

    @view.memoize
    def view_url(self, obj):
        """Generate view url."""
        return '/'.join([
            absoluteURL(obj, self.request),
            '',
        ])
