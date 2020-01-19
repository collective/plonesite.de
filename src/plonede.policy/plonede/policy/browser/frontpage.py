# -*- coding: utf-8 -*-
from plone import api
from plone.app.event.base import spell_date
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

import logging

logger = logging.getLogger('plonede.policy')


class FrontPageView(BrowserView):

    def __call__(self):
        self.plone_view = api.content.get_view('plone', self.context, self.request)
        return self.index()

    def news(self):
        results = []
        brains = api.content.find(
            portal_type='News Item',
            sort_on='created',
            sort_order='reverse',
            review_state='published',
            sort_limit=4,
            )[:4]
        for index, brain in enumerate(brains):
            obj = brain.getObject()
            if index == 0:
                width = 600
                height = 300
                css_class = 'image-inline img-fluid'
            else:
                width = 300
                height = 150
                css_class = 'image-inline img-fluid'

            scales = api.content.get_view(
                name='images',
                context=obj,
                request=self.request)
            scale = scales.scale(
                'image',
                width=width,
                height=height,
                direction='down')
            tag = scale.tag(css_class=css_class) if scale else None

            results.append({
                'title': brain.Title,
                'description': self.plone_view.cropText(brain.Description, 120),
                'description_short': self.plone_view.cropText(brain.Description, 80),
                'url': brain.getURL(),
                # 'src': brain.getURL(),
                'tag': tag,
                })
        return results

    def events(self):
        results = []
        brains = api.content.find(
            portal_type='Event',
            sort_on='start',
            sort_order='reverse',
            review_state='published',
            sort_limit=3,
            )[:3]
        for brain in brains:
            results.append({
                'title': brain.Title,
                'description': brain.Description,
                'url': brain.getURL(),
                'start': spell_date(brain.start),
            })
        return results

    def providers(self):
        portal = api.portal.get()
        providers_page = portal.get('providers')
        if providers_page:
            return providers_page