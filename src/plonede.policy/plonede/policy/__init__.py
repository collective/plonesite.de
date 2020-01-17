# -*- extra stuff goes here -*-
from OFS.SimpleItem import SimpleItem
from plone.app.upgrade.utils import alias_module
from zope.interface import Interface


class IBBB(Interface):
    pass


try:
    from collective.js.jqueryui.interfaces import IJqueryUILayer
    IJqueryUILayer  # noqa
except ImportError:
    alias_module('collective.js.jqueryui.interfaces.IJqueryUILayer', IBBB)


try:
    from App.interfaces import IPersistentExtra
    IPersistentExtra  # noqa
except ImportError:
    alias_module('App.interfaces.IPersistentExtra', IBBB)


try:
    from App.interfaces import IUndoSupport
    IUndoSupport  # noqa
except ImportError:
    alias_module('App.interfaces.IUndoSupport', IBBB)
