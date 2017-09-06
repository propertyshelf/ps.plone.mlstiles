# -*- coding: utf-8 -*-
"""Post install import steps for ps.plone.mlstiles."""

# python imports
import pkg_resources

# zope imports
from plone import api


def install_cover_support(context):
    """Register tiles collective.cover."""
    if not context.readDataFile('ps.plone.mlstiles.cover.txt'):
        return

    try:
        pkg_resources.get_distribution('collective.cover')
    except pkg_resources.DistributionNotFound:
        return

    tiles = [
        u'ps.plone.mlstiles.developments.collection',
        u'ps.plone.mlstiles.listings.collection',
        u'ps.plone.mlstiles.listings.recent',
        u'ps.plone.mlstiles.listings.featured',
        u'ps.plone.mlstiles.listings.search',
    ]
    calendar_tile = u'collective.cover.calendar'

    from collective.cover.controlpanel import ICoverSettings
    record = dict(interface=ICoverSettings, name='available_tiles')
    available_tiles = api.portal.get_registry_record(**record)
    try:
        available_tiles.remove(calendar_tile)
    except ValueError:
        pass  # no calendar tile found
    for tile in tiles:
        if tile not in available_tiles:
            available_tiles.append(tile)

    api.portal.set_registry_record(value=available_tiles, **record)
