# -*- coding: utf-8 -*-
from plone import api
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

import logging

logger = logging.getLogger('plonede.policy')


class FrontPageView(BrowserView):

    def __call__(self):
        # foo
        return self.index()

    def news(self):
        brains = api.content.find(
            portal_type='News Item',
            sort_on='effective',
            sort_order='reverse',
            review_state='published',
            )
