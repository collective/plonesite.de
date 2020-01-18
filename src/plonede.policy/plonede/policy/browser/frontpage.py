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
        results = []
        brains = api.content.find(
            portal_type='News Item',
            sort_on='effective',
            sort_order='reverse',
            review_state='published',
            sort_limit=4,
            )[:4]
        for brain in brains:
            obj = brain.getObject()
            # if getattr(obj.aq_base, 'image'):

            scales = api.content.get_view(
                name='images',
                context=obj,
                request=self.request)
            scale = scales.scale(
                'image',
                width=400,
                height=200,
                direction='down')
            tag = scale.tag() if scale else None

            # 64, 64,
            # src = obj.
            results.append({
                'title': brain.Title,
                'description': brain.Description,
                'url': brain.getURL(),
                # 'src': brain.getURL(),
                'tag': tag,
                })
        return results
