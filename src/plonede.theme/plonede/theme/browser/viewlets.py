from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from zope.viewlet.interfaces import IViewletManager


class OuterViewletManager(IViewletManager):
    """ A viewlet manager outside of visual-portal-wrapper  """


class TryMeViewlet(ViewletBase):
    """ A linkt to demo.plone.de
    """
    render = ViewPageTemplateFile("templates/tryme.pt")
