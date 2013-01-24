from Acquisition import aq_inner

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class RssView(BrowserView):
    
    template = ViewPageTemplateFile('templates/rss.pt')
    
    def __call__(self):
        self.request.set('disable_border', True)
        return self.template()