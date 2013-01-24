from zope.interface import implements
from zope.viewlet.interfaces import IViewlet

from Acquisition import aq_inner, aq_parent
from zope.interface import implements
from Products.CMFCore.utils import getToolByName

from Products.Five.browser import BrowserView
from plone.app.layout.viewlets.common import ViewletBase

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from bgp.HeaderImageViewlet.browser.interfaces import IHeaderImage
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot

class HeaderImageViewlet(ViewletBase):
    """ HeaderImageViewlet Viewlet
    """

    render = ViewPageTemplateFile('headerimageviewlet.pt')

    def getNextParentFolder(self, obj):
        while not IHeaderImage.providedBy(obj) and not IPloneSiteRoot.providedBy(obj):
            obj = aq_parent(obj)
        return IHeaderImage.providedBy(obj) and obj or None

    def update(self):
        self.header = None
        self.image = None
        self.type = None
        self.root = False
        headerimage = 1 
        context = self.context
        obj = self.getNextParentFolder(aq_inner(self.context))
        raw_header_image = getattr(context.aq_explicit,'headerimage',None)
        if raw_header_image:
            headerimage = raw_header_image
        if obj is not None:
            while not (getattr(context.aq_explicit,'headerimage',None)):
                obj = self.getNextParentFolder(aq_parent(obj))
                if obj is None:
                    break
            if obj is not None:
                headerimage = getattr(context.aq_explicit,'headerimage',None)
                if headerimage:
                    self.type = 'img'
                    self.header = '%s' % (headerimage.absolute_url())
        if not self.header:
            self.root = True
            urltool = getToolByName(aq_inner(self.context), 'portal_url')
            portal = urltool.getPortalObject()
            if 'headerimage' in portal.objectIds():
                self.header = '%s/headerimage' % urltool()
                self.type = 'img'

